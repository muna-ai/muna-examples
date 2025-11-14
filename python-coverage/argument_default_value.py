#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile, Parameter
from typing import Annotated

@compile(
    tag="@yusuf/default-args",
    description="Test default arguments.",
)
def predict(
    a: Annotated[float, Parameter.Numeric(description="First number.")],
    b: Annotated[float, Parameter.Numeric(description="Second number with default.")]=10.0,
    c: Annotated[float, Parameter.Numeric(description="Third number with default.")]=42.0
) -> Annotated[float, Parameter.Numeric(description="Sum of a, b, and c.")]:
    """
    Add three numbers where b has a default value of 10.0 and c has a default value of 42.0.
    """
    return a + b + c

if __name__ == "__main__":
    # Test with all arguments
    result1 = predict(5.0, 3.0, 2.0)
    print(f"predict(5.0, 3.0, 2.0) = {result1}")
    # Test with default argument for c
    result2 = predict(5.0, 3.0)
    print(f"predict(5.0, 3.0) = {result2}")
    # Test with default arguments for b and c
    result3 = predict(5.0)
    print(f"predict(5.0) = {result3}")
    print(f"\nExpected: 10.0, 50.0, and 57.0")
    print(f"Success: {result1 == 10.0 and result2 == 50.0 and result3 == 57.0}")