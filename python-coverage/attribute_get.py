# 
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile
from PIL import Image

@compile(
    tag="@yusuf/attribute-get",
    description="Test `attribute.get` support."
)
def get_image_size(image: Image.Image) -> tuple[int, int]:
    return image.size