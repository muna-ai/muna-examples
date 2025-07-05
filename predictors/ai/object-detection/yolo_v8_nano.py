#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "fxn",
#     "rich",
#     "torchvision",
#     "ultralytics"
# ]
# ///

from fxn import compile, Sandbox
from fxn.beta import OnnxInferenceMetadata
from PIL import Image
from pydantic import BaseModel, Field
from torch import inference_mode, randn, tensor, Tensor
from torch.nn import Module
from torchvision.ops import batched_nms, box_convert
from torchvision.transforms import functional as F
from torchvision.utils import draw_bounding_boxes
from ultralytics import YOLO

class Detection(BaseModel):
    x_center: float = Field(description="Normalized bounding box center X-coordinate.")
    y_center: float = Field(description="Normalized bounding box center Y-coordinate.")
    width: float = Field(description="Normalized bounding box width.")
    height: float = Field(description="Normalized bounding box height.")
    label: str = Field(description="Detection label.")
    confidence: float = Field(description="Detection confidence score.")

# Instantiate model
yolo = YOLO("yolov8n.pt")
model: Module = yolo.model
model.eval()
labels: dict[int, str] = model.names

# Dry run the model to prepare for export
model_args = [randn(1, 3, 640, 640)]
model(*model_args)

# Define predictor
@compile(
    tag="@ultralytics/yolo-v8-nano",
    description="Detect objects in an image with YOLO-v8 (nano).",
    access="private", # YOLO-v8 is under AGPL license
    sandbox=Sandbox()
        .pip_install("torch", "torchvision", index_url="https://download.pytorch.org/whl/cpu")
        .pip_install("ultralytics")
        .pip_install("opencv-python-headless"),
    metadata=[
        OnnxInferenceMetadata(
            model=model,
            model_args=model_args
        )
    ]
)
@inference_mode()
def detect_objects(
    image: Image.Image,
    *,
    min_confidence: float=0.25,
    max_iou: float=0.45
) -> list[Detection]:
    """
    Detect objects in an image with YOLO-v8 (nano).

    Parameters:
        image (PIL.Image): Input image.
        min_confidence (float): Minimum detection confidence.
        max_iou (float): Maximum intersection-over-union score before discarding smaller detections.

    Returns:
        list: Detected objects.
    """
    # Preprocess
    image_tensor, scale_factors = _preprocess_image(image, input_size=640)
    # Run model
    model_outputs = model(image_tensor[None])
    # Extract components
    logits: Tensor = model_outputs[0]                   # (1,84,8400)
    predictions = logits[0].T                           # (8400,84)
    boxes_cxcywh = predictions[:,:4] * scale_factors    # (8400,4)
    class_scores = predictions[:,4:]                    # (8400,80)
    max_scores, class_ids = class_scores.max(dim=1)     # (8400,), (8400,)
    # Filter by score
    confidence_mask = max_scores >= min_confidence
    filtered_boxes = boxes_cxcywh[confidence_mask]
    filtered_scores = max_scores[confidence_mask]
    filtered_class_ids = class_ids[confidence_mask]
    # Check if any detections remain
    if len(filtered_boxes) == 0:
        return []
    # Apply NMS
    boxes_xyxy = box_convert(
        filtered_boxes,
        in_fmt="cxcywh",
        out_fmt="xyxy"
    )
    keep_indices = batched_nms(
        boxes_xyxy,
        scores=filtered_scores,
        idxs=filtered_class_ids,
        iou_threshold=max_iou
    )
    # Select final detections
    final_boxes = filtered_boxes[keep_indices]
    final_scores = filtered_scores[keep_indices]
    final_class_ids = filtered_class_ids[keep_indices]
    # Create detection objects
    detections = [
        _create_detection(box, class_id=class_id, score=score)
        for box, class_id, score
        in zip(final_boxes, final_class_ids, final_scores)
    ]
    # Return
    return detections

def _preprocess_image(
    image: Image.Image,
    *,
    input_size: int
) -> tuple[Tensor, Tensor]:
    """
    Preprocess an image for inference by downscaling and padding it to have a square aspect.
    """
    # Compute scaled size and padding
    image_width, image_height = image.size
    ratio = min(input_size / image_width, input_size / image_height)
    scaled_width = int(image_width * ratio)
    scaled_height = int(image_height * ratio)
    image_padding = [0, 0, input_size - scaled_width, input_size - scaled_height]
    # Downscale and pad image
    image = image.convert("RGB")
    image = F.resize(image, [scaled_height, scaled_width])
    image = F.pad(image, image_padding, fill=114)
    # Create tensors
    image_tensor = F.to_tensor(image)
    scaled_sizes = tensor([scaled_width, scaled_height, scaled_width, scaled_height])
    # Return
    return image_tensor, scaled_sizes.reciprocal()

def _create_detection(
    box: Tensor,
    *,
    class_id: Tensor,
    score: Tensor
) -> Detection:
    label = labels[class_id.item()]
    detection = Detection(
        x_center=box[0].item(),
        y_center=box[1].item(),
        width=box[2].item(),
        height=box[3].item(),
        label=label,
        confidence=score.item()
    )
    return detection

def _render_detections(
    image: Image.Image,
    detections: list[Detection]
) -> Image.Image:
    image = image.convert("RGB")
    image_tensor = F.to_tensor(image)
    boxes_cxcywh = tensor([[
        detection.x_center * image.width,
        detection.y_center * image.height,
        detection.width * image.width,
        detection.height * image.height
    ] for detection in detections])
    boxes_xyxy = box_convert(
        boxes_cxcywh,
        in_fmt="cxcywh",
        out_fmt="xyxy"
    )
    labels = [detection.label for detection in detections]
    result_tensor = draw_bounding_boxes(
        image_tensor,
        boxes=boxes_xyxy,
        labels=labels,
        width=8,
        font="Arial",
        font_size=int(0.015 * image.width)
    )
    return F.to_pil_image(result_tensor)

if __name__ == "__main__":
    from rich import print_json
    # Detect objects
    image = Image.open("media/vehicles.jpg")
    detections = detect_objects(image)
    # Print detections
    print_json(data=[det.model_dump() for det in detections])
    # Show annotated image
    annotated_image = _render_detections(image, detections)
    annotated_image.show()