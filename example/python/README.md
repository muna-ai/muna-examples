# Function Playground for Python
This sample project illustrates how to run a compiled Python function in your Python apps.

## Setup Instructions
First, install Function for Python:
```bash
# Run this in Terminal
$ pip install --upgrade fxn
```

Next, [create an access key](https://fxn.ai/settings/developer) then update the [predict.py](predict.py) script 
with it:
```py
# Create Function client
fxn = Function(access_key="<ACCESS KEY>")
```

Then in the call to `fxn.predictions.create`, specify your compiled predictor's tag:
```py
# Make a prediction
prediction = fxn.predictions.create(
    tag="@fxn/greeting",       # replace this with your predictor tag
    inputs={ "name": "Yusuf" }
)
```

Finally, run the script:
```bash
# Run the script
$ python3 predict.py
```