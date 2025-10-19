#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "muna",
#     "typer"
# ]
# ///

from muna import Muna
from pathlib import Path
from PIL import Image
from rich import print, print_json
from typer import Argument, Option, Typer
from typing import Annotated

app = Typer()

@app.command()
def detect(
    image: Annotated[Path, Argument(help="Path to the input image.", exists=True, dir_okay=False, resolve_path=True)],
    access_key: Annotated[str, Option(help="Muna access key.", envvar="MUNA_ACCESS_KEY")]
):
    """
    Detect objects in the given image.
    """
    # Load the image
    image = Image.open(image)
    # Run an object detection predictor on the image
    muna = Muna(access_key=access_key)
    prediction = muna.predictions.create(
        tag="@baidu/rt-detr",
        inputs={ "image": image,  }
    )
    # Check for errors
    if prediction.error:
        print(f"[bright_red]Error: {prediction.error}[/bright_red]")
        return
    # Print the results
    print_json(data=prediction.results[0])

if __name__ == "__main__":
    app()