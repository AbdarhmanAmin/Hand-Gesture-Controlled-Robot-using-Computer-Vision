# Hand-Gesture-Controlled-Robot-using-Computer-Vision
🤖 Hand Gesture Controlled Robot using Computer Vision
📌 Project Overview

This project presents a Hand Gesture Controlled Robot powered by Computer Vision. The system enables real-time robot control using hand gestures captured through a camera, eliminating the need for traditional controllers.

By leveraging gesture recognition, the robot can interpret specific hand movements and translate them into motion commands such as forward, backward, left, and right.

🎯 Objectives

Build an intuitive human-robot interaction system.

Control a mobile robot wirelessly using hand gestures.

Apply computer vision techniques in a real-world robotics application.

Achieve real-time performance with reliable communication.

🧠 System Architecture

1. Gesture Detection Layer

Captures live video stream via webcam.

Detects and tracks hand landmarks.

Classifies gestures into predefined commands.

2. Processing Layer

Converts gestures into control signals.

Maps each gesture to a robot movement.

3. Communication Layer

Sends commands wirelessly to the robot.

4. Robot Control Layer

Receives signals.

Controls motors accordingly via microcontroller.

🛠️ Technologies & Tools Used

Python

OpenCV

MediaPipe (Hand Tracking)

Arduino IDE

ESP32

Motor Driver (L298N / L293D)

DC Motors & Chassis Kit

Serial / Wireless Communication

✋ Supported Gestures & Actions
Gesture	Robot Action
Open Palm	Stop
Fist	Move Forward
Thumb Left	Turn Left
Thumb Right	Turn Right
Two Fingers	Move Backward

(Gestures can be customized and expanded.)

🚧 Challenges Faced

During the development of this project, several technical challenges were encountered:

🔵 Bluetooth Module Issues

Initially, we used a Bluetooth module (HC-05/HC-06) for wireless communication between the computer and the robot. However, we faced multiple problems such as:

Unstable connection.

High latency in command transmission.

Frequent disconnections.

Limited range and interference issues.

We attempted troubleshooting by:

Replacing the Bluetooth module.

Reconfiguring baud rates.

Testing different wiring setups.

Reprogramming communication protocols.

Despite these efforts, the performance was still unreliable for real-time gesture control.

🟢 Solution — Switching to ESP32

To overcome these limitations, we migrated to ESP32.

This significantly improved the system because ESP32 provides:

Built-in Wi-Fi & Bluetooth.

Faster processing capability.

More stable wireless communication.

Lower latency in real-time control.

After reprogramming the communication layer using ESP32, the robot achieved smooth and responsive gesture-based control.

⚙️ How It Works

The webcam captures the user’s hand gestures.

MediaPipe detects hand landmarks.

The system classifies the gesture.

A command is generated.

The command is sent wirelessly via ESP32.

The robot executes the movement.


🔌 Hardware Connections

ESP32 → Motor Driver IN Pins

Motor Driver → DC Motors

External Battery → Motor Driver Power

ESP32 powered via USB / Battery

(Detailed circuit diagram can be added here.)

📊 Results

Real-time gesture detection achieved.

Stable wireless control using ESP32.

Smooth robot navigation based on hand gestures.

Reduced latency compared to Bluetooth module.

🚀 Future Improvements

Add more complex gestures.

Implement obstacle avoidance.

Deploy on Raspberry Pi for full onboard processing.

Integrate deep learning gesture classification.

Add mobile app control.

👨‍💻 Author
Abdarhman Magdy Mohamed
Faculty of Computers & Artificial Intelligence
Artificial Intelligence Department
AI Engineer | Artificial Intelligence Enthusiast
