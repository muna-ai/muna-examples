#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import compile
from math import pi

@compile(
    tag="@yusuf/global-return",
    description="Test global return."
)
def get_pi () -> float:
    return pi