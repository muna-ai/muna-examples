package app.fxn.playground.demos

import ai.fxn.fxn.Function
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

@Composable
fun Greeting (navController: NavController, modifier: Modifier = Modifier) {
    var name by remember { mutableStateOf("") }
    var result by remember { mutableStateOf("") }
    var error by remember { mutableStateOf("") }
    val focusManager = LocalFocusManager.current
    val fxn = Function("<ACCESS KEY>")

    fun createPrediction () {
        // Hide the keyboard
        focusManager.clearFocus()
        // Create prediction
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val prediction = fxn.predictions.create(
                    "@fxn/greeting",
                    mapOf("name" to name)
                )
                result = prediction.results!![0] as String
            } catch (ex: Exception) {
                error = ex.message.toString()
            }
        }
    }

    Box(modifier = modifier.fillMaxSize()) {

        // Back button
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

        // Demo
        Column(
            modifier = modifier.fillMaxSize().padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            // Title
            Text(text = "Greeting", fontSize = 24.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(16.dp))
            // Name input field
            OutlinedTextField(
                value = name,
                onValueChange = { name = it },
                label = { Text("Enter your name") }
            )
            Spacer(modifier = Modifier.height(16.dp))
            // Button
            Button(onClick = { createPrediction() }) {
                Text("Predict")
            }
            Spacer(modifier = Modifier.height(16.dp))
            // Result display
            Text(text = result, fontSize = 18.sp)
            Text(text = error, fontSize = 18.sp, color = Color.Red)
        }
    }
}