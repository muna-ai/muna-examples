#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

# We handle input variable reassignment naturally.
# If it is a heterogenous reassignment, then 
# we promote the type of the input to `std::variant<std::monostate, TOld, TNew>`.

from muna import compile
import numpy as np

@compile(
    tag="@yusuf/hoist-input",
    description="Hoisting an input variable."
)
def hoist_input(a: np.int64) -> np.int64:
    a = a + a
    a = 4 * a
    return a