#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from math import e, pi
from muna import compile

@compile(
    tag="@yusuf/global-use",
    description="Test using multiple globals."
)
def do_math(a: float) -> float:
    return a * pi + e