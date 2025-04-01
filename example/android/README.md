# Function Playground for Android
This sample project illustrates how to run a compiled Python function in your Android apps.

## Setup Instructions
In a few steps:

### Specifying your Access Key
First, open up the project in Android Studio. Then in 
[`MainActivity.kt`](app/src/main/java/app/fxn/playground/MainActivity.kt), add your access key in the `Greeting` 
method:
```kt
// Add your access key here
val fxn = Function("<ACCESS KEY>")
```



### Specifying your Predictor Tag
In [`MainActivity.kt`](app/src/main/java/app/fxn/playground/MainActivity.kt), find the 
`Greeting.createPrediction` function and specify your predictor tag in the call to `fxn.predictions.create`:
```kt
val prediction = fxn.predictions.create(
    "@fxn/greeting",      // replace this with your predictor tag
    mapOf("name" to name)
)
```

You will also need to specify your access key and predictor tag in the [`build.gradle.kts`](app/build.gradle.kts) 
file to [embed the predictor](https://docs.fxn.ai/concepts#sandboxing-on-android-and-ios) into your app at build-time:
```kt
fxn {
  accessKey = "<ACCESS KEY>"              // add your access key here
  embeds.addAll(
    FunctionEmbed(tag = "@fxn/greeting")  // replace this with your predictor tag
  )
}
```

### Running the Sample
Build the app to your device and try it out!