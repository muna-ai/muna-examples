#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile, Parameter
from typing import Annotated

@compile(
    tag="@yusuf/tuple-return",
    description="Test returning a tuple."
)
def propose_greetings(
    name: Annotated[str, Parameter.Generic(description="User name.")],
    nickname: Annotated[str, Parameter.Generic(description="User nickname.")]
) -> tuple[
    Annotated[str, Parameter.Generic(description="Greeting using the user's name.")],
    Annotated[str, Parameter.Generic(description="Greeting using the user's nickname.")]
]:
    greeting_1 = f"Hello {name}"
    greeting_2 = f"What's up {nickname}?"
    return greeting_1, greeting_2