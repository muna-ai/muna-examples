#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

# Function has limited support for recursive functions, primarily due to challenges in type propagation.
# Recursive functions **must** have return type annotations, and for now those types must be simple.
# In the future, we might add proper support for recursion with fixed point iteration or Algorithm W.

@compile(
    tag="@yusuf/recursion",
    description="Test recursion support."
)
def factorial(n: int) -> int:
    match n:
        case 0: return 1
        case 1: return 1
        case _: return n * factorial(n - 1)