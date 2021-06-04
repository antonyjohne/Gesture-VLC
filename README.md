# Gesture VLC 🖐️

GVLC is an Python Program that tracks Hand movement and controls VLC Media Player using Hand Gestures. The program uses the Mediapipe module to track Hand movement and PyAutoGUI to execute key presses when a Hand Gesture is recognized. The Gestures are NOT trained using Machine Learning Classifers but make use of simple program logic.


## What I Learned
- Common methods and function of OpenCV Module
- Image Manipulation and Feature Extraction
- How To Work with the Mediapipe module and Protobuf Outputs
- Logic Statements for Gesture Recognition
- Building your own Image Module for Code Reusability

## Instructions

Install the required dependencies using `pip install -r Modules.txt`

For the program to work, ensure that the Media Player is running in the foreground.
Press the 'Esc' key with the Hand Tracking Window open in the foreground to Quit the Program.

Gestures:
You must first Activate Gesture Recognition by making an Open Hand before showing Gestures.

- 🖐️ Open Hand: Gesture Recognition Active
- ✊ Closed Fist: Pause/Play
- ☝️ 1 Finger Open (Swipe Horizontally): Skip Forward/Backward
- ✌️ 2 Finger Open (Swipe Vertically): Volume Increase/Decrease
- 👌 3 Finger Open: Mute
- 🤘 Rock Sign: Close Program
