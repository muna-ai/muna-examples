#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

# We handle local variable reassignment naturally.
# If it is a homogenous reassignment, we simply assign the new value to the variable.
# If it is a heterogenous reassignment, we promote the type 
# of the variable to `std::variant<std::monostate, TOld, TNew>`.

from muna import compile
import numpy as np

@compile(
    tag="@yusuf/hoist-reassign",
    description="Hoisting a reassigned variable."
)
def hoist_reassign(a: np.int64) -> np.int64:
    result = a + a
    result = result + result
    result = result + result
    return result