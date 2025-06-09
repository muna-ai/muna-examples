#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import compile, Sandbox
from fxn.beta import OnnxInferenceMetadata
from PIL import Image
from torch import inference_mode, randn, Tensor
from torchvision.models.segmentation import deeplabv3_resnet50, DeepLabV3_ResNet50_Weights
from torchvision.transforms import functional as F

weights = DeepLabV3_ResNet50_Weights.DEFAULT
model = deeplabv3_resnet50(weights=weights).eval()

@compile(
    tag="@google/deeplab-v3",
    description="Semantic image segmentation with atrous convolutions.",
    sandbox=Sandbox().pip_install("torch==2.6.0", "torchvision==0.21"),
    metadata=[
        OnnxInferenceMetadata(
            model=model,
            model_args=[randn(1, 3, 520, 520)]
        )
    ]
)
@inference_mode()
def predict (image: Image.Image) -> tuple[str, float]:
    # Preprocess image
    image = F.resize(image, [520])
    image_tensor = F.to_tensor(image)
    image_tensor = F.normalize(
        image_tensor,
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
    # Run model
    output_dict: dict[str, Tensor] = model(image_tensor[None])
    output_tensor = output_dict["out"]
    # Return
    return output_tensor

if __name__ == "__main__":
    image = Image.open("test/media/runner.jpg")
    result = predict(image)
    print(result)