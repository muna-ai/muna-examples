# Pose Detection Predictors
This directory contains a few predictors that detect human poses within an image using popular pose detection models.

## Running a Pose Detection Sample
The first step is to run the prediction function directly. First, we recommend installing [uv](https://docs.astral.sh/uv/getting-started/installation/) as it simplifies working with Python dependencies. Once `uv` is installed, you can run 
any of the pose detection predictors by simply executing the script directly:
```bash
# Run this in Terminal
$ uv run predictors/ai/pose-detection/yolo_v8_pose_xlarge.py
```

`uv` will automatically install any required Python packages then run the script.

## Compiling the Predictor with Function
Once you have chosen a pose detection predictor to use in your application, first update the predictor tag of the 
detection function with your Function username:
```diff
# Define predictor
@compile(
-   tag="@ultralytics/yolo-v8-pose-xlarge",
+   tag="@<YOUR FUNCTION USERNAME>/yolo-v8-pose-xlarge",
    ...
)
def detect_poses(...) -> list[Pose]:
    ...
```

Next, compile the Python code with Function:
```bash
# Run this in Terminal
$ fxn compile --overwrite predictors/ai/pose-detection/yolo_v8_pose_xlarge.py
```

Function will generate and compile self-contained, cross-platform native code that runs the pose detection function.

## Running the Predictor
Once compiled, you can run the predictor on any device using our client libraries. For example, run the predictor in 
the command line:
```bash
# Run this in Terminal
$ fxn predict @<YOUR FUNCTION USERNAME>/yolo-v8-pose-xlarge --image @./path/to/image.jpg
```

Function compiles predictors to run on Android, iOS, macOS, Linux, visionOS, WebAssembly, and Windows. We provide
client libraries to run these predictors for JavaScript, Kotlin, Android, React Native, Unity, and more.
[Learn more](https://docs.fxn.ai/predictions/create).