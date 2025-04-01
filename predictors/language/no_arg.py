#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import compile

def get_pi ():
    return 3.14 # very rough approx

@compile(
    tag="@yusuf/no-arg",
    description="Test compiling a function with no arguments."
)
def compute_two_pi () -> float:
    return 2 * get_pi()