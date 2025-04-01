#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import compile

@compile(
    tag="@yusuf/fstring",
    description="Test string interpolation with f-strings."
)
def greeting (name: str) -> str:
    return f"Hey there {name}! We're glad you're trying out Function and we hope you like it 😉"