#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

# Once lowered, the types of `result_a` and `result_b` MUST match.
# Specifically, we need to see a deterministic ordering of variant member types.

@compile(
    tag="@yusuf/list-concat-hetero",
    description="Test heterogenous list concatenation."
)
def predict(name: str, age: int) -> list:
    names = [name, name, name, name]
    ages = [age, age, age, age]
    result_a = names + ages
    result_b = ages + names # C++ types for `result_a` and `result_b` MUST match
    return len(result_a) + len(result_b)