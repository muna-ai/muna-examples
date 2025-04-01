# Compiler Example
This example demonstrates the process of compiling a Python function then running it in the following frameworks: 
- React (Browser, Node.js)
- React Native (Android, iOS)
- Kotlin in Android Studio (Android)
- Swift in Xcode (iOS)
- Python (Linux, macOS, Windows)
- Unity Engine (Android, iOS, Linux, macOS, visionOS, WebGL, Windows)

## Setup Instructions
First, download the Function CLI:
```bash
# 💥 Install the Function CLI
$ pip install --upgrade fxn
```

Next, create an [access key](https://fxn.ai/settings/developer) and login to the CLI:
```bash
# 🔥 Login to the Function CLI
$ fxn auth login <ACCESS KEY>
```

## Compiling your Function
The [predictor.py](predictor.py) module defines a prediction function `greeting`. Update the predictor `tag` 
with your Function username:
```py
from fxn import compile

@compile(
    tag="@your-username/greeting", # replace `your-username`
    description="Say a friendly greeting."
)
def greeting (name: str) -> str:
    return f"Hey there {name}! We're glad you're using Function and we hope you like it."
```

Compile it using the `fxn compile` CLI command:
```bash
# Compile the `greeting` function
$ fxn compile predictor.py
```

## Using the Function
See the respective directories for more information.