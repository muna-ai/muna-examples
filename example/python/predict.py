# 
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from fxn import Function

# Create Function client
fxn = Function(access_key="<ACCESS KEY>")

# Make a prediction
prediction = fxn.predictions.create(
    tag="@fxn/greeting",
    inputs={ "name": "Yusuf" }
)

# Print the result
print(prediction.results[0])