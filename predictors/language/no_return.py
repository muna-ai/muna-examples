#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import compile

@compile(
    tag="@yusuf/no-return",
    description="Test returning nothing."
)
def no_return () -> None:
    pass