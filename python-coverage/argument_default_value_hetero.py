#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/argument-default-value-heterogenous",
    description="Test support for arguments with default values of a different type.",
)
def predict(items: list[str]="nothing here") -> int:
    # `items` should be std::variant<std::string, std::vector<std::string>>
    return len(items)