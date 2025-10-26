# 
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/assign-argument-hetero",
    description="Assigning heterogenous values to a function argument."
)
def assign_argument_hetero(x: int) -> str:
    # Since `x` is assigned to a string, its C++ type needs to be 
    # updated to `std::variant<int32_t, std::string>`. This update 
    # must be reflected in the function prototype.
    x = "hello world"
    return x