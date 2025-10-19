#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/while",
    description="Test while-loop support."
)
def decrement(number: float) -> float:
    while number > 2:
        number = number - 1
    return number