# 
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/assign-local-variant",
    description="Assigning heterogenous values to a local variable."
)
def assign_variant() -> str:
    x = 10
    x = "hello world"
    return x