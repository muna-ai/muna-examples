#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import compile

@compile(
    tag="@yusuf/tuple-return",
    description="Test returning a tuple."
)
def propose_greetings (name: str, nickname: str) -> tuple[str, str]:
    greeting_1 = f"Hello {name}"
    greeting_2 = f"What's up {nickname}?"
    return greeting_1, greeting_2