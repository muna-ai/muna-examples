#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "fxn",
#     "torch",
#     "torchvision",
#     "opencv-python-headless",
#     "huggingface_hub",
# ]
# ///

from cv2 import applyColorMap, cvtColor, COLOR_BGR2RGB, COLORMAP_INFERNO
from fxn import compile, Sandbox
from numpy import ceil, ndarray, uint8
from PIL import Image
from torch import inference_mode, Tensor
from torch.nn.functional import interpolate
from torchvision.transforms import functional as F

from depth_anything.dpt import DepthAnything

# Create model
model = DepthAnything.from_pretrained("LiheYoung/depth_anything_vitl14").eval()

def resize_image ( # lower_bound only!!
    image_tensor: Tensor,
    target_width: int=518,
    target_height: int=518,
    ensure_multiple_of: int=14
) -> Tensor:
    """
    Resize image tensor while keeping aspect ratio and ensuring dimensions are multiples of a constant.
    """
    _, _, h, w = image_tensor.shape
    # Compute lower bound scale factor
    scale_height = target_height / h
    scale_width = target_width / w
    scale = scale_width if scale_width > scale_height else scale_height
    # Calculate new dimensions
    new_height = int(scale * h)
    new_width = int(scale * w)
    # Ensure dimensions are multiples of ensure_multiple_of
    new_height = int(ceil(new_height / ensure_multiple_of) * ensure_multiple_of)
    new_width = int(ceil(new_width / ensure_multiple_of) * ensure_multiple_of)
    # Ensure we meet minimum size requirements
    new_height = max(new_height, target_height)
    new_width = max(new_width, target_width)
    # Resize using bilinear interpolation
    resized = interpolate(
        image_tensor,
        size=(new_height, new_width),
        mode="bilinear",
        align_corners=False
    )
    # Return
    return resized

def colorize_depth (depth_tensor: Tensor) -> Image.Image:
    """
    Colorize a depth tensor using OpenCV's COLORMAP_INFERNO heatmap.
    
    Args:
        depth_tensor: Depth tensor with shape (H, W)
    
    Returns:
        Image.Image: Colorized depth map as PIL Image
    """
    # Convert to numpy and normalize to 0-255 range
    depth_np = depth_tensor.cpu().numpy()
    depth_normalized: ndarray = (depth_np - depth_np.min()) / (depth_np.max() - depth_np.min()) * 255.0
    depth_uint8 = depth_normalized.astype(uint8)
    # Apply OpenCV colormap
    depth_colored = applyColorMap(depth_uint8, COLORMAP_INFERNO)
    # Convert BGR to RGB
    depth_colored = cvtColor(depth_colored, COLOR_BGR2RGB)
    # Convert to PIL Image
    return Image.fromarray(depth_colored)

@compile(
    tag="@tiktok/depth-anything",
    description="Depth estimation using Depth Anything model.",
    sandbox=Sandbox().pip_install(
        "torch==2.6.0",
        "torchvision==0.21",
        "opencv-python-headless",
        "huggingface_hub==0.17.3",
        index_url="https://download.pytorch.org/whl/cpu"
    ),
    access="unlisted"
)
@inference_mode()
def predict_depth (image: Image.Image) -> Tensor:
    """
    Estimate metric depth from an image using Depth Anything model.
    
    Parameters:
        image (PIL.Image): Input image.
    
    Returns:
        Tensor: Metric depth tensor with shape (H, W).
    """
    # Preprocess image
    width, height = image.size
    image = image.convert("RGB")
    image_tensor = F.to_tensor(image)   # (3,H,W)
    image_tensor = image_tensor[None]   # (1,3,H,W)
    resized_tensor = resize_image(image_tensor)
    normalized_tensor = F.normalize(
        resized_tensor, 
        mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225]
    )
    # Run inference
    depth_batch = model(normalized_tensor)
    # Interpolate back to original size
    depth_batch = interpolate(
        depth_batch[None],
        size=(height, width),
        mode="bilinear",
        align_corners=False
    )
    depth = depth_batch[0,0]
    # Return
    return depth

if __name__ == "__main__":
    import rich
    # Predict metric depth
    image = Image.open("room.jpg")
    depth_tensor = predict_depth(image)
    rich.print(f"Metric depth shape: {depth_tensor.shape} range: [{depth_tensor.min().item():.2f}, {depth_tensor.max().item():.2f}]")
    # Colorize depth tensor and save
    depth_img = colorize_depth(depth_tensor)
    depth_img.save("test_depth_output.png")