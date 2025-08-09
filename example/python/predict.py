# 
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import Muna

# Create a Muna client
muna = Muna(access_key="<ACCESS KEY>")

# Make a prediction
prediction = muna.predictions.create(
    tag="@fxn/greeting",
    inputs={ "name": "Yusuf" }
)

# Print the result
print(prediction.results[0])