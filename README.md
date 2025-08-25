# Muna Compiler
![Muna logo](https://raw.githubusercontent.com/muna-ai/.github/main/logo_wide.png)

Muna compiles stateless Python functions to run anywhere.
This project is a playground for testing the Muna compiler. Over time, we expect to open-source more 
and more of the compiler infrastructure in this project.

## Setup Instructions
First, install Muna for Python:
```sh
# Run this in Terminal
$ pip install --upgrade muna
```

Next, head over to the [Muna dashboard](https://muna.ai/settings/developer) to generate an access key. 
Once generated, sign in to the CLI:
```sh
# Login to the Muna CLI
$ muna auth login <ACCESS KEY>
```

## Compiling a Function
The [`predictors`](/predictors) directory contains several prediction functions, ranging from very simple functions to 
AI inference with PyTorch. Internally, we use these functions to test language and library coverage in the compiler.
To compile a function, first update the predictor tag with your Muna username:
```py
@compile(
    tag="@username/some-function", # replace `username` with your Muna username
    description="Compile a cool function."
)
def grader (score: float) -> str:
    ...
```

Next, use the Muna CLI to compile the function, providing the path to the module where the function is defined:
```sh
# Compile the decorated function at the module path
$ muna compile --overwrite path/to/module.py
```

The compiler will load the entrypoint function, create a remote sandbox, and compile the function:

![compiling a function](media/fma.gif)

## Inspecting the Generated Code
Once you compile a function, you can download the generated C++ code:
```sh
# Retrieve the generated C++ source code for a given predictor
$ muna source --predictor @username/some-function
```

> [!NOTE]
> Because our compiler can generate hundreds of implementations for a given predictor, we recommend 
> using `muna source --prediction <id>` to get the generated C++ code for a specific prediction. The 
> provided `id` **must have been provided directly by our API**.

> [!WARNING]
> The generated C++ code is provided for reference and cannot be compiled independently, as it depends on 
> additional scaffolding provided by the Muna compiler toolchain.

## Useful Links
- [Discover predictors to use in your apps](https://muna.ai/explore).
- [Join our Slack community](https://muna.ai/slack).
- [Check out our docs](https://docs.muna.ai).
- Learn more about us [on our blog](https://blog.muna.ai).
- Reach out to us at [hi@muna.ai](mailto:hi@muna.ai).

Muna is a product of [NatML Inc](https://github.com/natmlx).
