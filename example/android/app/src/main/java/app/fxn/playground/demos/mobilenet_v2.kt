package app.fxn.playground.demos

import ai.fxn.fxn.Function
import ai.fxn.fxn.types.Image
import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.util.Log
import android.util.Size
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.annotation.OptIn
import androidx.camera.core.CameraSelector
import androidx.camera.core.ExperimentalGetImage
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.content.ContextCompat
import androidx.lifecycle.LifecycleOwner
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.navigation.NavController
import com.google.common.util.concurrent.ListenableFuture
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

@OptIn(ExperimentalGetImage::class)
@Composable
fun MobileNetv2 (navController: NavController) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current
    val cameraProviderFuture = remember { ProcessCameraProvider.getInstance(context) }
    val fxn = Function("<ACCESS KEY>")
    val predictorTag = "@yusuf/mobilenet-v2"
    var predictorLoaded = remember { false }
    var mainText by remember { mutableStateOf("") }
    var subText by remember { mutableStateOf("") }
    // Preload the predictor
    LaunchedEffect(Unit) {
        withContext(Dispatchers.IO) {
            try {
                fxn.predictions.create(predictorTag, emptyMap())
                predictorLoaded = true
            } catch (ex: Exception) {
                Log.e("Function", "Failed to preload predictor with error: ${ex}")
            }
        }
    }
    // Keep track of the camera permission state
    var hasCameraPermission by remember { mutableStateOf(
        ContextCompat.checkSelfPermission(
            context,
            Manifest.permission.CAMERA
        ) == PackageManager.PERMISSION_GRANTED
    ) }
    val launcher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        hasCameraPermission = isGranted
    }
    LaunchedEffect(Unit) {
        if (!hasCameraPermission) {
            launcher.launch(Manifest.permission.CAMERA)
        }
    }
    // Handle camera preview images
    val onCameraImage: (ImageProxy) -> Unit = remember {
        { imageProxy: ImageProxy ->
            try {
                if (predictorLoaded) {
                    // Create a prediction input image from the camera image
                    val cameraImage = imageProxy.image
                    val image = Image.fromImage(cameraImage, imageProxy.imageInfo.rotationDegrees)
                    // Create a prediction
                    val prediction = fxn.predictions.create(
                        predictorTag,
                        mapOf("image" to image)
                    )
                    // Display the results
                    if (prediction.results != null) {
                        mainText = prediction.results!![0] as String
                        subText = (prediction.results!![1] as Float).toString()
                    } else {
                        mainText = "Error occurred"
                        subText = prediction.error!!
                    }
                }
            } finally {
                imageProxy.close()
            }
        }
    }
    // Render the page
    Box(modifier = Modifier.fillMaxSize()) {
        if (hasCameraPermission) {
            // Camera view
            AndroidView(
                factory = { ctx ->
                    val previewView = PreviewView(ctx)
                    setupCameraPreview(
                        context = ctx,
                        lifecycleOwner = lifecycleOwner,
                        cameraProviderFuture = cameraProviderFuture,
                        previewView = previewView,
                        imageHandler = onCameraImage
                    )
                    previewView
                },
                modifier = Modifier.fillMaxSize()
            )
            // Add back button in top-left corner
            IconButton(
                onClick = { navController.popBackStack() },
                modifier = Modifier
                    .align(Alignment.TopStart)
                    .padding(16.dp)
                    .background(
                        color = Color.Black.copy(alpha = 0.3f),
                        shape = CircleShape
                    )
            ) {
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                    contentDescription = "Back",
                    tint = Color.White
                )
            }
            // Overlay to display classification results
            Box(
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .fillMaxWidth()
                    .padding(bottom = 72.dp)
                    .background(Color.Black.copy(alpha = 0.6f))
                    .padding(vertical = 16.dp)
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(
                        text = mainText,
                        color = Color.White,
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Bold,
                        textAlign = TextAlign.Center
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = subText,
                        color = Color.White,
                        fontSize = 16.sp,
                        textAlign = TextAlign.Center
                    )
                }
            }
        } else {
            // Show message when camera permission is not granted
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(16.dp),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text("Camera permission is required for this demo")
                Spacer(Modifier.height(16.dp))
                Button(onClick = { launcher.launch(Manifest.permission.CAMERA) }) {
                    Text("Request Permission")
                }
                Spacer(Modifier.height(16.dp))
                Button(onClick = { navController.popBackStack() }) {
                    Text("Go Back")
                }
            }
        }
    }
}

private fun setupCameraPreview (
    context: Context,
    lifecycleOwner: LifecycleOwner,
    cameraProviderFuture: ListenableFuture<ProcessCameraProvider>,
    previewView: PreviewView,
    imageHandler: (ImageProxy) -> Unit
) {
    val executor = ContextCompat.getMainExecutor(context)
    cameraProviderFuture.addListener({
        // Setup preview
        val cameraProvider = cameraProviderFuture.get()
        val preview = Preview.Builder().build().also {
            it.setSurfaceProvider(previewView.surfaceProvider)
        }
        // Setup callback to handle images
        val imageAnalysis = ImageAnalysis.Builder()
            .setTargetResolution(Size(1280, 720))
            .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
            .build()
        imageAnalysis.setAnalyzer(executor, imageHandler)
        try {
            cameraProvider.unbindAll()
            cameraProvider.bindToLifecycle(
                lifecycleOwner,
                CameraSelector.DEFAULT_BACK_CAMERA,
                preview,
                imageAnalysis
            )
        } catch (e: Exception) {
            Log.e("CameraX", "Use case binding failed", e)
        }
    }, executor)
    Unit
}