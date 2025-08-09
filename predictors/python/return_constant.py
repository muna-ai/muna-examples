#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/constant-return",
    description="Test constant return."
)
def constant_string() -> str:
    return "Hello from Function"