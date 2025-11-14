#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

# During codegen, we don't preserve any distinction between a function and a (global) lambda.
# As such, we lower `doubler` to a regular C++ function. Local lambdas (i.e. defined within a function) 
# on the other hand are preserved, and emitted as regular C++ lambda expressions.

from muna import compile

doubler = lambda x: x << 1

@compile(
    tag="@yusuf/lambda-global",
    description="Test invoking lambda expressions in the global scope."
)
def double_number(num: int) -> int:
    return doubler(num)