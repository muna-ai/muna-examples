#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile

@compile(
    tag="@yusuf/return-emoji",
    description="Testing support for UTF-8 strings."
)
def get_emoji() -> tuple[str, str, int]:
    text = "👁️👄👁️"
    length = len(text)
    individual_chars = [foo for foo in text]
    return text, individual_chars[-1], length