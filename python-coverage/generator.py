#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile
from typing import Iterator

@compile(
    tag="@yusuf/generator",
    description="Test compiling generator functions."
)
def split_sentence(sentence: str) -> Iterator[str]:
    parts = sentence.split()
    for part in parts:
        yield part