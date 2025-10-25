#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile
import numpy as np

@compile(
    tag="@yusuf/iadd",
    description="In-place add."
)
def predict() -> int:
    current_length = 1
    for _ in range(10):
        current_length +=  1
    return current_length