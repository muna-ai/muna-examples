#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import compile

@compile(
    tag="@yusuf/if",
    description="Test if-statement support."
)
def grader (score: float) -> str:
    if score < 0.2:
        grade = "low"
    elif score < 0.8:
        grade = "medium"
    else:
        grade = "high"
    return grade