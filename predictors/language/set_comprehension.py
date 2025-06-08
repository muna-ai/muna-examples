#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import compile

@compile(
    tag="@fxn/set-comprehension",
    description="Test set comprehension support."
)
def predict () -> int:
    names = ["Yusuf", "Terri", "Rhea", "Muna", "Terri"]
    unique_names = { "hello " + name for name in names }
    return len(unique_names)