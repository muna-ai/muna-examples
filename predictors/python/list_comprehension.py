#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@fxn/list-comprehension",
    description="Test list comprehension support."
)
def predict(count: int) -> list:
    return [f"The number is {x}" for x in range(count)]