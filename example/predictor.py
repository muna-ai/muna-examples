#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import compile

@compile(
    tag="@your-username/greeting", # replace with your Function username
    description="Say a friendly greeting."
)
def greeting (name: str) -> str:
    return f"Hey there {name}! We're glad you're using Function and we hope you like it."