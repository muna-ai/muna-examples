#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/ternary-hetero",
    description="Test heterogenous ternary assignment support."
)
def can_drink(age: int) -> str:
    return f"you can drink because you are over {age} years old" if age >= 21 else False