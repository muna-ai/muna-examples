#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import compile

@compile(
    tag="@yusuf/for",
    description="Test for-loop support."
)
def loop (number: float) -> float:
    for i in range(10):
        number += i
    return number