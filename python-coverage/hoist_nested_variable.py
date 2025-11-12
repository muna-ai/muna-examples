#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

# One major difference between Python and C++ is the topics of (block) scopes.
#
# In Python, there is no concept of scopes within a function. If you define a variable 
# within an indented block (e.g. `if` or `while` statement body), the variable remains 
# accessible outside that scope.
#
# But in C++, variables defined within a scope cannot be accessed outside that scope.
# As such, we simply hoist all variables that are accessed outside their defining scope; 
# and promote their types from `T` to `std::optional<T>`.

from muna import compile
import numpy as np

@compile(
    tag="@yusuf/hoist-nested-variable",
    description="Hoist a nested variable."
)
def hoist_nested_variable() -> np.int64:
    for i in range(2):
        result = 20
    return result