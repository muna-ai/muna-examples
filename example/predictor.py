#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@your-username/greeting", # replace with your Muna username
    description="Say a friendly greeting."
)
def greeting(name: str) -> str:
    return f"Hey there {name}! We're glad you're using Muna and we hope you like it."