#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "fxn",
#     "rich",
#     "torch",
#     "torchvision",
# ]
# ///

from fxn import compile, Sandbox
from fxn.beta import OnnxInferenceMetadata
from PIL import Image
from torch import argmax, randn, softmax
from torchvision.models import resnet50, ResNet50_Weights
from torchvision.transforms import functional as F

weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights).eval()

@compile(
    tag="@pytorch/resnet-50",
    description="Classify an image with ResNet-50.",
    sandbox=Sandbox().pip_install(
        "torch==2.6.0",
        "torchvision==0.21",
        index_url="https://download.pytorch.org/whl/cpu"
    ),
    metadata=[
        OnnxInferenceMetadata(
            model=model,
            model_args=[randn(1, 3, 256, 256)]
        ),
    ],
    access="unlisted"
)
def classify(image: Image.Image) -> tuple[str, float]:
    """
    Classify an image with ResNet-50.

    Returns:
        str: Classification label.
        float: Classification score.
    """
    # Preprocess
    image = image.convert("RGB")
    image = F.resize(image, 256)
    image = F.center_crop(image, 256)
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
    score = scores[0, idx].item()
    label = weights.meta["categories"][idx]
    # Return
    return label, score

if __name__ == "__main__":
    import rich
    image = Image.open("media/cat.jpg")
    label, score = classify(image)
    rich.print(label, score)