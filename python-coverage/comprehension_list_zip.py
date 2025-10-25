#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/list-comprehension-zip",
    description="Test list comprehension support on zip iterators."
)
def predict(name: str) -> list[str]:
    names = [name, name, name, name]
    ages = [10, 12, 14, 16]
    greetings = [f"{name} is {age} years old" for name, age in zip(names, ages)]
    return greetings