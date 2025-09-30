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

from muna import compile, Parameter, Sandbox
from muna.beta import OnnxRuntimeInferenceMetadata
from PIL import Image
from torch import randn, argmax, inference_mode, softmax
from torchvision.models import alexnet, AlexNet_Weights
from torchvision.transforms.functional import center_crop, normalize, resize, to_tensor
from typing import Annotated

weights = AlexNet_Weights.DEFAULT
model = alexnet(weights=weights).eval()

@compile(
    tag="@pytorch/alexnet",
    description="Classify an image with AlexNet.",
    access="public",
    sandbox=Sandbox().pip_install("torchvision", index_url="https://download.pytorch.org/whl/cpu"),
    metadata=[
        OnnxRuntimeInferenceMetadata(
            model=model,
            model_args=[randn(1, 3, 224, 224)]
        )
    ]
)
@inference_mode()
def classify_image(
    image: Annotated[Image.Image, Parameter.Generic(description="Input image.")]
) -> tuple[
    Annotated[str, Parameter.Generic(description="Classification label.")],
    Annotated[float, Parameter.Numeric(description="Classification score.", range=(0., 1.))]
]:
    """
    Classify an image with AlexNet.
    """
    # Preprocess image
    image = image.convert("RGB")
    image = resize(image, 256)
    image = center_crop(image, 224)
    image_tensor = to_tensor(image)
    normalized_tensor = normalize(
        image_tensor,
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
    # Run model
    logits = model(normalized_tensor[None])
    # Post-process outputs
    scores = softmax(logits, dim=1)
    idx = argmax(scores, dim=1)
    score = scores[0, idx].item()
    label = weights.meta["categories"][idx]
    # Return
    return label, score

if __name__ == "__main__":
    image = Image.open(f"media/cat.jpg")
    label, score = classify_image(image)
    print(label, score)