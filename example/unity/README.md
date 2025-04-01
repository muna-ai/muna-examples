# Function Playground for Unity Engine
This sample project illustrates how to run a compiled Python function in Unity Engine.

## Setup Instructions
In a few steps:

### Specifying your Access Key
First, open up the project in Unity. Then add your access key to `Project Settings > Function`:

![Adding your access key](https://raw.githubusercontent.com/fxnai/fxn3d/main/settings.gif)

### Adding your Predictor Tag
Open the [`Assets/Predict.cs`](Assets/Predict.cs) script and update the `PredictorTag` field with your predictor tag:
```cs
// Replace this with your predictor tag
private const string PredictorTag = "@my-username/greeting";
```

### Running the Sample
Finally, press play!