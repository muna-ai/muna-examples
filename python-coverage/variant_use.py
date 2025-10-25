#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/variant-use",
    description="Using a variant is (currently) hard! But we support them all the same."
)
def get_variant() -> int:
    result = [10, 11] if 0.4 > 0.6 else "hello"
    count = len(result)
    return count