//
//  ContentView.swift
//  Compiler Playground
//
//  Created by Yusuf Olokoba on 11/8/2024.
//  Copyright © 2025 NatML Inc. All rights reserved.
//

import FunctionSwift
import SwiftUI

struct ContentView: View {
    
    @State private var name: String = ""
    @State private var loading: Bool = false
    @State private var greeting: String?
    private let fxn = Function(accessKey: ContentView.accessKey)

    var body: some View {
        VStack (spacing: 20) {

            AsyncImage(url: URL(string: "https://fxn.ai/icon.png")) { image in
                    image
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: 100, height: 100)
            } placeholder: {
                ProgressView() // Show a placeholder while loading
            }
            
            Text("Greeting Demo")
                .font(.title)
                .fontWeight(.bold)
            
            TextField("Enter your name...", text: $name)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()
            
            if loading {
                ProgressView()
            }

            Button(action: {
                Task {
                    await predict()
                }
            }) {
                Text("Predict")
                    .fontWeight(.semibold)
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(name.isEmpty ? Color.gray : Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(999)
            }
            .padding(.horizontal)
            .disabled(name.isEmpty)
            .opacity(name.isEmpty ? 0.5 : 1.0)
            
            if greeting != nil {
                Text(greeting!)
                    .font(.body)
                    .padding()
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color(.systemGray6)) // Light gray background
                    .cornerRadius(8)
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(Color(.systemGray4), lineWidth: 1) // Border color
                    )
                    .padding(.horizontal)
                    .padding(.top, 10)
            }
            
        }
        .padding()
    }
    
    func predict () async {
        // Hide keyboard
        UIApplication.shared.sendAction(
            #selector(UIResponder.resignFirstResponder),
            to: nil,
            from: nil,
            for: nil
        )
        // Predict
        do {
            loading = true
            let prediction = try await fxn.predictions.create(
                tag: "@fxn/greeting",
                inputs: ["name": name]
            )
            greeting = prediction.results![0] as? String
            loading = false
        } catch {
            print("\(error)")
        }
    }

    private static var accessKey: String? {
        guard let path = Bundle.main.path(forResource: "fxn", ofType: "xcconfig") else {
            print("Function config file not found")
            return nil
        }
        do {
            let contents = try String(contentsOfFile: path, encoding: .utf8)
            var result: String? = nil
            contents.enumerateLines { line, _ in
                let parts = line.split(separator: "=", maxSplits: 1, omittingEmptySubsequences: true)
                if parts.count == 2 {
                    let key = String(parts[0]).trimmingCharacters(in: .whitespaces)
                    var value = String(parts[1]).trimmingCharacters(in: .whitespaces)
                    if value.hasPrefix("\"") && value.hasSuffix("\"") {
                        value = String(value.dropFirst().dropLast())
                    }
                    if key == "FXN_ACCESS_KEY" {
                        result = value
                    }
                }
            }
            return result
        } catch {
            print("Error reading config file: \(error)")
            return nil
        }
    }
}

#Preview {
    ContentView()
}
