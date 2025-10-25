#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile
from pydantic import BaseModel
from typing import Literal

class Pet(BaseModel):
    legs: int
    sound: Literal["bark", "meow"]

@compile(
    tag="@yusuf/pydantic-model",
    description="Testing support for creating Pydantic models."
)
def create_pet(leg_count: int, noise: str) -> Pet:
    return Pet(legs=leg_count, sound=noise)