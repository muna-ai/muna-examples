#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/list-comprehension-predicate",
    description="Test list comprehension support with a predicate."
)
def predict(count: int) -> list:
    return [f"The number is {x}" for x in range(count) if x % 2]