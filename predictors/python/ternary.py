#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import compile

@compile(
    tag="@yusuf/ternary",
    description="Test ternary assignment support."
)
def can_drink (age: int) -> str:
    return f"you can drink because you are over {age} years old" if age >= 18 else "you cannot drink"