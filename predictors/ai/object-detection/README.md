# Object Detection Predictors
This folder contains a few predictors that detect images within an image using popular object detection models.

## Running a Detection Sample
The first step is to run the prediction function directly. First, we recommend installing [uv](https://docs.astral.sh/uv/getting-started/installation/) as it simplifies working with Python dependencies. Once `uv` is installed, you can run 
any of the object detection predictors by simply executing the script directly:
```bash
# Run this in Terminal
$ uv run predictors/ai/object-detection/yolo_v8_nano.py
```

`uv` will automatically install any required Python packages then run the script.

## Compiling the Predictor with Function
Once you have chosen an object detection model to use in your application, first update the predictor tag of the 
detection function with your Function username:
```diff
# Define predictor
@compile(
-   tag="@ultralytics/yolo-v8-nano",
+   tag="@<YOUR FUNCTION USERNAME>/yolo-v8-nano",
    ...
)
def detect_objects(...) -> list[Detection]:
    ...
```

Next, compile the Python code with Function:
```bash
# Run this in Terminal
$ fxn compile --overwrite predictors/ai/object-detection/yolo_v8_nano.py
```

Function will generate and compile self-contained native code (C++, Rust, etc) that runs the object detection function.

## Running the Predictor
Once compiled, you can run the predictor on any device using our client libraries. For example, run the predictor in 
the command line:
```bash
# Run this in Terminal
$ fxn predict @<YOUR FUNCTION USERNAME>/yolo-v8-nano --image @./path/to/image.jpg
```

Function compiles predictors to run on Android, iOS, macOS, Linux, visionOS, WebAssembly, and Windows. We provide
client libraries to run these predictors for JavaScript, Kotlin, Android, React Native, Unity, and more.
[Learn more](https://docs.fxn.ai/predictions/create).