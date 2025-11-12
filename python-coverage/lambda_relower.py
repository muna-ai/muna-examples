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

# One detail of note: we can emit the same lambda multiple times if its input types differ between invocations.
# The below example illustrates this: we emit `doubler` twice, one taking an `int32_t` and the other taking a `float`.

@compile(
    tag="@yusuf/lambda-relower",
    description="Test relowering a lambda expression with distinct input types."
)
def calculate_weird_num(num: int) -> float:
    doubler = lambda x: x * 2
    num_a = doubler(num)        # `doubler` emitted as `std::function<int32_t(int32_t)>;`
    num_b = doubler(num + 1.5)  # `doubler` emitted as `std::function<float(float)>;`
    return num_a + num_b