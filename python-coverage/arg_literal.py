#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile
from typing import Literal

Direction = Literal["north", "east", "south", "west"]

@compile(
    tag="@yusuf/arg-literal",
    description="Test literal argument support."
)
def direction_to_heading_angle(direction: Direction) -> float:
    """
    Convert a direction constant to a heading angle in degrees (clockwise).
    """
    match direction:
        case "north":   return 0
        case "east":    return 90
        case "south":   return 180
        case "west":    return 270