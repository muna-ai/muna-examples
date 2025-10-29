# Text-to-Speech Predictors
This directory contains a few predictors that generate speech audio from text using popular text-to-speech models.

## Running a Text-to-Speech Sample
The first step is to run the prediction function directly. First, we recommend installing [uv](https://docs.astral.sh/uv/getting-started/installation/) as it simplifies working with Python dependencies. Once `uv` is installed, you can run 
any of the text-to-speech predictors by simply executing the script directly:
```bash
# Run this in Terminal
$ uv run text-to-speech/kitten_tts.py
```

`uv` will automatically install any required Python packages then run the script.

## Compiling the Predictor
Once you have chosen a text-to-speech predictor to use in your application, first update the predictor tag of the 
generation function with your Muna username:
```diff
# Define predictor
@compile(
-   tag="@kitten-ml/kitten-tts",
+   tag="@<YOUR MUNA USERNAME>/kitten-tts",
    ...
)
def generate_speech(...) -> ndarray:
    ...
```

Next, compile the Python code with Muna:
```bash
# Run this in Terminal
$ muna compile --overwrite text-to-speech/kitten_tts.py
```

Muna will generate and compile a self-contained executable binary that generates speech audio from input text.

> [!TIP]
> You can also use pre-compiled text-to-speech predictors on [Muna](https://muna.ai/explore).

## Running the Predictor
Once compiled, you can run the predictor on any device using our client libraries. For example, run the predictor in 
the command line:
```bash
# Run this in Terminal
$ muna predict @USERNAME/kitten-tts --text "This speech was generated with Muna."
```

> [!TIP]
> Muna compiles predictors to run on Android, iOS, macOS, Linux, visionOS, WebAssembly, and Windows. We provide
> client libraries to run these predictors for JavaScript, Kotlin, Android, React Native, Unity, and more.
> [Learn more](https://docs.muna.ai/predictions/create).