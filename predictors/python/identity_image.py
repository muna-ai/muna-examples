#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile
from PIL import Image

@compile(
    tag="@yusuf/identity-image",
    description="Test returning an input image parameter as-is."
)
def identity(image: Image.Image) -> Image.Image:
    return image