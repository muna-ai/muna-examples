/* 
*   Function
*   Copyright © 2025 NatML Inc. All rights reserved.
*/

using UnityEngine;
using UnityEngine.UI;
using Function;

[Function.Function.Embed(PredictorTag)]
public class Predict : MonoBehaviour {

    public Text text;

    // Replace this with your predictor tag
    private const string PredictorTag = "@fxn/greeting";

    private async void Start () {
        var fxn = FunctionUnity.Create();
        var predictions = await fxn.Predictions.Create(
            tag: PredictorTag,
            inputs: new () { ["name"] = "Yusuf" }
        );
        text.text = predictions.results[0] as string;
    }
}
