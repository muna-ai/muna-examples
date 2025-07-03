#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import compile, Sandbox
from fxn.beta import OnnxInferenceMetadata
from PIL import Image
from torch import randn, argmax, softmax
from torchvision.models import regnet_y_8gf, RegNet_Y_8GF_Weights
from torchvision.transforms.functional import center_crop, normalize, resize, to_tensor

weights = RegNet_Y_8GF_Weights.DEFAULT
model = regnet_y_8gf(weights=weights).eval()

@compile(
    tag="@pytorch/regnet-y-8gf",
    description="Classify an image with RegNet-Y (8GF).",
    access="public",
    sandbox=Sandbox().pip_install("torchvision", index_url="https://download.pytorch.org/whl/cpu"),
    metadata=[
        OnnxInferenceMetadata(
            model=model,
            model_args=[randn(1, 3, 224, 224)]
        )
    ]
)
def classify(image: Image.Image) -> tuple[str, float]:
    """
    Classify an image with RegNet-Y (8GF).

    Parameters:
        image (PIL.Image): Input image.

    Returns:
        str: Classification label.
        float: Classification score.
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
    scores = softmax(logits, dim=1)
    idx = argmax(scores, dim=1)
    score = scores[0, idx].item()
    label = weights.meta["categories"][idx]
    # Return
    return label, score

if __name__ == "__main__":
    image = Image.open(f"media/cat.jpg")
    label, score = classify(image)
    print(label, score)