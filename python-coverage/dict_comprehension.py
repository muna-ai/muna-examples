#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/dict-comprehension",
    description="Test dictionary comprehension support."
)
def predict(count: int) -> dict:
    return { x: f"The number is {x}" for x in range(count) }