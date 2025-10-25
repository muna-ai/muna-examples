#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/list-comprehension-nested",
    description="Test nested list comprehension support."
)
def predict(count: int) -> list:
    return [f"The numbers are {x} and {y}" for x in range(count) for y in range(count)]