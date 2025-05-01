package app.fxn.playground

import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import app.fxn.playground.ui.components.DemoItem

@Composable
fun HomeScreen (navController: NavController) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = "Function Compiler Demos",
            style = MaterialTheme.typography.headlineSmall,
            modifier = Modifier.padding(bottom = 16.dp)
        )

        DemoItem(
            title = "Greeting Demo",
            description = "Preview camera feed using CameraX API",
            onClick = { navController.navigate("greeting") }
        )

        DemoItem(
            title = "MobileNet v2 Demo",
            description = "Realtime image classification with the MobileNet v2 vision model.",
            onClick = { navController.navigate("mobilenet-v2") }
        )
    }
}