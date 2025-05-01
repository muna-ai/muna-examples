package app.fxn.playground.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import app.fxn.playground.HomeScreen
import app.fxn.playground.demos.Greeting
import app.fxn.playground.demos.MobileNetv2

@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = "home") {
        composable("home") {
            HomeScreen(navController = navController)
        }
        composable("greeting") {
            Greeting(navController = navController)
        }
        composable("mobilenet-v2") {
            MobileNetv2(navController = navController)
        }
    }
}