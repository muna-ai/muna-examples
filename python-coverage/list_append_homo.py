#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/list-append-homo",
    description="Append items to a homogenous list."
)
def predict() -> list:
    result = [2]
    result.append(4)
    result.insert(0, 5)
    return result