#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import compile
from math import e, pi

@compile(
    tag="@yusuf/global-use",
    description="Test multiple global usage."
)
def do_math (a: float) -> float:
    return a * pi + e