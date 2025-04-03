#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from enum import IntEnum
from fxn import compile

class Direction (IntEnum):
    North = 0
    East = 1
    South = 2
    West = 3

@compile(
    tag="@yusuf/enum",
    description="Test enumeration support."
)
def direction_to_heading_angle (direction: Direction) -> float:
    """
    Convert a direction constant to a heading angle in degrees (clockwise).
    """
    return direction * 90.