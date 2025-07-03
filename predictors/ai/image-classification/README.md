# Image Classification Predictors
This folder contains a few predictors that classify images using popular image classification models.

## Running a Classification Sample
The first step is to run the prediction function directly. First, we recommend installing [uv](https://docs.astral.sh/uv/getting-started/installation/) as it simplifies working with Python dependencies. Once `uv` is installed, you can run 
any of the image classification predictors by simply executing the script directly:
```bash
# Run this in Terminal
$ uv run predictors/ai/image-classification/resnet_50.py
```

`uv` will automatically install any required Python packages then run the script.

## Compiling the Predictor with Function
Once you have chosen an image classification predictor to use in your application, first update the predictor tag of the 
classification function with your Function username:
```diff
# Define predictor
@compile(
-   tag="@pytorch/resnet-50",
+   tag="@<YOUR FUNCTION USERNAME>/resnet-50",
    ...
)
def classify(...) -> tuple[str, float]:
    ...
```

Next, compile the Python code with Function:
```bash
# Run this in Terminal
$ fxn compile --overwrite predictors/ai/image-classification/resnet_50.py
```

Function will generate and compile self-contained native code (C++, Rust, etc) that runs the image classification function.

## Running the Predictor
Once compiled, you can run the predictor on any device using our client libraries. For example, run the predictor in 
the command line:
```bash
# Run this in Terminal
$ fxn predict @<YOUR FUNCTION USERNAME>/resnet-50 --image @./path/to/image.jpg
```

Function compiles predictors to run on Android, iOS, macOS, Linux, visionOS, WebAssembly, and Windows. We provide
client libraries to run these predictors for JavaScript, Kotlin, Android, React Native, Unity, and more.
[Learn more](https://docs.fxn.ai/predictions/create).