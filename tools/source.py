#
#   Function
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from argparse import ArgumentParser
from datetime import datetime
from fxn import Function
from os import environ
from pathlib import Path
from pydantic import BaseModel, Field

parser = ArgumentParser("Function: Retrieve Source Code")
parser.add_argument("--prediction", type=str, required=True, help="Prediction identifier.")
parser.add_argument("--output", type=Path, default=Path("predictor.json"), help="Predictor source output path.")
parser.add_argument(
    "--access-key",
    type=str,
    default=environ.get("FXN_ACCESS_KEY"),
    help="Function access key. You MUST have source code access. Reach out to sales@fxn.ai for more info."
)

class _Implementation (BaseModel):
    tag: str = Field(description="Predictor tag.")
    target: str = Field(description="Implementation target identifier.")
    code: str = Field(description="Implementation source code.")
    created: datetime = Field(description="Date created.")
    compiled: datetime = Field(description="Date compiled.")
    latency: float = Field(description="Compilation time in milliseconds.")

def main ():
    args = parser.parse_args()
    fxn = Function(access_key=args.access_key)
    implementation = fxn.client.request(
        method="GET",
        path=f"/predictions/{args.prediction}/implementation",
        response_type=_Implementation
    )
    output_path: Path = args.output
    code_path = output_path.parent / f"{output_path.stem}.cpp" # we generate C++ for now, may switch to Rust
    output_path.write_text(implementation.model_dump_json(indent=2, exclude=["code"]))
    code_path.write_text(implementation.code)

if __name__ == "__main__":
    main()