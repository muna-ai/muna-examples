# Function Compiler
![function logo](https://raw.githubusercontent.com/fxnai/.github/main/logo_wide.png)

[![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdiscord.com%2Fapi%2Finvites%2Fy5vwgXkz2f%3Fwith_counts%3Dtrue&query=%24.approximate_member_count&logo=discord&logoColor=white&label=Function%20community)](https://discord.gg/fxn)

Function compiles stateless Python functions to run natively cross-platform.
This project is a playground for testing Function's compiler. Over time, we expect to open-source more 
and more of the compiler infrastructure in this project.

## Setup Instructions
First, install Function for Python:
```sh
# Install Function for Python
$ pip install --upgrade fxn
```

Next, head over to the [Function dashboard](https://fxn.ai/settings/developer) to generate an access key. 
Once generated, sign in to the CLI:
```sh
# Sign in to the Function CLI
$ fxn auth login <ACCESS KEY>
```

## Compiling a Function
The [predictors](/predictors) directory contains several prediction functions, ranging from very simple functions to 
AI inference with PyTorch. Internally, we use these functions to test language and library coverage in the compiler.
To compile a function, first update the predictor tag with your Function username:
```py
@compile(
    tag="@username/some-function", # replace `username` with your Function username
    description="Compile a cool function."
)
def grader (score: float) -> str:
    ...
```

Next, use the Function CLI to compile the function, providing the path to the module where the function is defined:
```sh
# Compile the decorated function at the module path
$ fxn compile path/to/module.py
```

The compiler will load the entrypoint function, create a remote sandbox, and compile the function:

![compiling a function](media/fma.gif)

## Inspecting the Generated Code
Once you compile a function, you can download the generated C++ code:
```sh
# Retrieve the generated C++ source code for a given predictor
$ fxn source --predictor @username/some-function
```

> [!NOTE]
> Because our compiler can generate hundreds of implementations for a given predictor, we recommend 
> using `fxn source --prediction <id>` to get the generated C++ code for a specific prediction. The 
> provided `id` **must have been provided directly by our API**.

> [!WARNING]
> The generated C++ code is provided for reference and cannot be compiled independently, as it depends on 
> additional scaffolding provided by the Function compiler toolchain.

## Useful Links
- [Discover predictors to use in your apps](https://fxn.ai/explore).
- [Join our Discord community](https://discord.gg/fxn).
- [Check out our docs](https://docs.fxn.ai).
- Learn more about us [on our blog](https://blog.fxn.ai).
- Reach out to us at [stdin@fxn.ai](mailto:stdin@fxn.ai).

Function is a product of [NatML Inc](https://github.com/natmlx).