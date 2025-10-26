#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

# Muna currently has partial support for lambda expressions.
# We can trace through lambdas, and even lower calls to lambdas.
# The challenge is in treating them as objects:
# In Python, you can pass around a lambda, add it to a list, add arbitrary attributes, and so on.
# In native code, we can only make a lambda concrete by attaching types to it.
# Hence for now we support invoking lambdas, but not treating them as plain objects.

from muna import compile

@compile(
    tag="@yusuf/lambda",
    description="Test lambda expression support."
)
def double_number(num: int) -> int:
    doubler = lambda x: x * 2
    return doubler(num)