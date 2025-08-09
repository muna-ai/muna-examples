#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "muna",
#     "rich",
#     "torchvision",
# ]
# ///

from muna import compile, Sandbox
from muna.beta import OnnxRuntimeInferenceMetadata
from PIL import Image
from torch import argmax, inference_mode, softmax, randn
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights
from torchvision.transforms import functional as F

weights = MobileNet_V2_Weights.DEFAULT
model = mobilenet_v2(weights=weights).eval()

@compile(
    tag="@pytorch/mobilenet-v2",
    description="Classify an image with MobileNet v2.",
    access="public",
    sandbox=Sandbox().pip_install(
        "torch==2.6.0",
        "torchvision==0.21",
        index_url="https://download.pytorch.org/whl/cpu"
    ),
    metadata=[
        OnnxRuntimeInferenceMetadata(
            model=model,
            model_args=[randn(1, 3, 224, 224)]
        ),
    ]
)
@inference_mode()
def classify_image(image: Image.Image) -> tuple[str, float]:
    """
    Classify an image with MobileNet v2.
    
    Parameters:
        image (PIL.Image): Input image.

    Returns:
        str: Classification label.
        float: Classification score.
    """
    # Preprocess
    image = image.convert("RGB")
    image = F.resize(image, 224)
    image = F.center_crop(image, 224)
    image_tensor = F.to_tensor(image)
    normalized_tensor = F.normalize(
        image_tensor,
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
    # Run model
    logits = model(normalized_tensor[None])
    # Postprocess
    scores = softmax(logits, dim=1)
    idx = argmax(scores, dim=1)
    score = scores[0,idx].item()
    label = weights.meta["categories"][idx]
    # Return
    return label, score

if __name__ == "__main__":
    import rich
    image = Image.open("media/cat.jpg")
    label, score = classify_image(image)
    rich.print(label, score)