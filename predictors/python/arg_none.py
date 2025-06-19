#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import compile

def get_pi ():
    return 3.14 # very rough approx

@compile(
    tag="@yusuf/arg-none",
    description="Test no argument support."
)
def compute_two_pi () -> float:
    return 2 * get_pi()