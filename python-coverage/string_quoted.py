#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/quoted-string",
    description="Testing lowering strings with quotes."
)
def quoted_string() -> str:
    return 'He said "What?"'