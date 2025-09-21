#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

# NOTE: In order to run and/or compile this model, you must clone Depth Anything V2 into the current working directory.
# Run `git clone https://github.com/DepthAnything/Depth-Anything-V2.git` then run/compile this script.

# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "huggingface_hub",
#     "muna",
#     "opencv-python-headless",
#     "torchvision"
# ]
# ///

from cv2 import applyColorMap, cvtColor, COLOR_BGR2RGB, COLORMAP_INFERNO
from huggingface_hub import hf_hub_download
from muna import compile, Parameter, Sandbox
from muna.beta import OnnxRuntimeInferenceMetadata
from numpy import ndarray, uint8
from pathlib import Path
from PIL import Image
import sys
from torch import inference_mode, load as torch_load, randn
from torchvision.transforms import functional as F
from typing import Annotated

# Import Depth Anything V2
sys.path.insert(0, str(Path.cwd() / "Depth-Anything-V2"))
from depth_anything_v2.dpt import DepthAnythingV2

# Grab the DepthAnythingV2 vits/small model from HF
weights_path = hf_hub_download(
    repo_id="depth-anything/Depth-Anything-V2-Small",
    filename="depth_anything_v2_vits.pth"
)
weights = torch_load(weights_path, map_location="cpu")
model = DepthAnythingV2(encoder="vits", features=64, out_channels=[48, 96, 192, 384])
model.load_state_dict(weights)
model.eval()

@compile(
    tag="@tiktok/depth-anything-v2-small",
    description="Estimate metric depth from an image with Depth Anything V2 (small).",
    access="public",
    sandbox=Sandbox()
        .pip_install("torch", "torchvision", index_url="https://download.pytorch.org/whl/cpu")
        .pip_install("huggingface_hub", "opencv-python-headless")
        .run_commands("git clone https://github.com/DepthAnything/Depth-Anything-V2.git"),
    metadata=[
        OnnxRuntimeInferenceMetadata(model=model, model_args=[randn(1, 3, 224, 224)]) # INCOMPLETE # Dynamic shapes??
    ]
)
@inference_mode()
def estimate_depth(
    image: Annotated[Image.Image, Parameter.Generic(description="Input image.")]
) -> Annotated[ndarray, Parameter.Generic(description="Metric depth tensor with shape (H,W).")]:
    """
    Estimate metric depth from an image with Depth Anything V2 (small).
    """
    # Preprocess
    src_width, src_height = image.size
    dst_width, dst_height = _get_resize_dimensions(
        image,
        smaller_side_length=518,
        ensure_multiple_of=14
    )
    image = image.convert("RGB")
    image = F.resize(image, (dst_height, dst_width))
    image_tensor = F.to_tensor(image)
    normalized_tensor = F.normalize(
        image_tensor,
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
    # Predict depth
    depth_batch = model(normalized_tensor[None])
    # Upsample depth
    depth_batch = F.resize(depth_batch, (src_height, src_width))
    depth = depth_batch[0].numpy()
    # Return
    return depth

def _get_resize_dimensions(
    image: Image.Image,
    *,
    smaller_side_length: int=518,
    ensure_multiple_of: int=14
) -> tuple[int, int]:
    """
    Calculate target dimensions while maintaining aspect ratio using a default
    minimum of 518. Dimensions must be evenly divisible by 14.
    """
    # Aspect scale
    src_width, src_height = image.size
    aspect_ratio = src_width / src_height
    if src_width <= src_height:
        dst_width = smaller_side_length
        dst_height = int(smaller_side_length / aspect_ratio)
    else:
        dst_height = smaller_side_length
        dst_width = int(smaller_side_length * aspect_ratio)
    # Enforce multiple both dimensions
    dst_width = (dst_width // ensure_multiple_of) * ensure_multiple_of
    dst_height = (dst_height // ensure_multiple_of) * ensure_multiple_of
    # Return
    return dst_width, dst_height

def _visualize_depth(depth: ndarray) -> Image.Image:
    """
    Colorize a depth array using OpenCV's COLORMAP_INFERNO heatmap.
    """
    depth_range = depth.max() - depth.min()
    depth_normalized = (depth - depth.min()) / depth_range
    depth_uint8 = (depth_normalized * 255).astype(uint8)
    depth_colored = applyColorMap(depth_uint8, COLORMAP_INFERNO)
    depth_colored = cvtColor(depth_colored, COLOR_BGR2RGB)
    return Image.fromarray(depth_colored)

if __name__ == "__main__":
    # Predict
    image = Image.open(f"media/city.jpg")
    depth = estimate_depth(image)
    # Visualize
    depth_image = _visualize_depth(depth)
    depth_image.show()