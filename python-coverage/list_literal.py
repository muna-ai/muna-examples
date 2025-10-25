#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/list-literal",
    description="List construction with a literal expression."
)
def predict(base: float) -> list[float]:
    return [base, base ** 2, base ** 3, base ** 4]