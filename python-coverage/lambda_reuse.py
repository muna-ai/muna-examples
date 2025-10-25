#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

# Muna currently has partial support for lambda expressions.
# We can trace through lambdas, and even lower calls to lambdas. The challenge is in treating them as objects.
# In Python, you can pass around a lambda, add it to a list, add arbitrary attributes, and so on.
# In native code, we can only make a lambda concrete by attaching types to it.
# Hence for now we support invoking lambdas, but not treating them as plain objects.

@compile(
    tag="@yusuf/lambda-reuse",
    description="Test reusing a lambda expression."
)
def calculate_weird_num(num: int) -> int:
    doubler = lambda x: x * 2
    num_a = doubler(num)
    num_b = doubler(num + 1)
    return num_a + num_b