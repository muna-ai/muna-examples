#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile, Sandbox

@compile(
    tag="@anon/utf-string",
    description="Iterate over a UTF8 string, return length and last char."
)
def process_utf8_string(text: str) -> tuple[int, str]:
    length = len(text)
    individual_chars = [foo for foo in text]
    return length, individual_chars[-1]

if __name__ == "__main__":
    length, last = process_utf8_string("ðɪs ɪz ɐ tɛst €")
    print(f"There are {length} characters, last is {last}")