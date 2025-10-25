#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/return-emoji",
    description="Testing support for returning UTF-8 strings."
)
def get_emoji() -> str:
    return "👁️👄👁️"