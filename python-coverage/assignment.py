# 
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/assignment",
    description="Testing assignment."
)
def assign_variable(num: int) -> int:
    x = num
    return x