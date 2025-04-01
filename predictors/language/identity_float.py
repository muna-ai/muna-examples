#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import compile

@compile(
    tag="@yusuf/identity-float",
    description="Test returning an input floating-point parameter as-is."
)
def identity (value: float) -> float:
    return value