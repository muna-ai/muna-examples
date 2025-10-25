#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/return-variant-of-tuples",
    description="Return a variant of tuples."
)
def have_conversation(friendly: bool) -> str: # should be std::variant<bool, std::tuple<std::string, int32_t>> in C++
    if friendly:
        return "Hello!", 25
    else:
        return False