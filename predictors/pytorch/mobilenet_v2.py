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
# ]
# ///

from fxn import compile, Sandbox
from fxn.beta import CoreMLInferenceMetadata, ONNXInferenceMetadata
from PIL import Image
from torch import argmax, inference_mode, softmax, randn
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights
from torchvision.transforms import functional as F

weights = MobileNet_V2_Weights.DEFAULT
model = mobilenet_v2(weights=weights)
model_example_input = randn(1, 3, 224, 224) # used to lower the model during compilation
model.eval()

@compile(
    tag="@yusuf/mobilenet-v2",
    description="Image classifier trained on ImageNet 1k.",
    sandbox=Sandbox().pip_install("torch", "torchvision"),
    metadata=[
        CoreMLInferenceMetadata(model=model, model_args=(model_example_input,)),
        ONNXInferenceMetadata(model=model, model_args=(model_example_input,))
    ]
)
@inference_mode()
def predict (image: Image.Image) -> tuple[str, float]:
    """
    Classify an image.
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
    scores = softmax(logits, dim=1)
    idx = argmax(scores, dim=1)
    score = scores[0,idx].item()
    label = weights.meta["categories"][idx]
    # Return
    return label, score

if __name__ == "__main__":
    image = Image.open("./media/cat.jpg")
    print(predict(image))