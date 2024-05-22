# Eye_Cursor

## Pre-Overview
This is a fork of the original application by Skanda2007. The point is to bring the functionality to mind and use normal modern code. The author of the fork is using Python for the first time (Lua knowledge helps), so if something is wrong, write to me in Discord.

## Overview
This is a program built to help control the cursor of any laptop or desktop using python. it uses **Mediapipe from Google**, **PyAutoGUI** and **OpenCV**. OpenCV is used to enable the camera of the system to take input. Mediapipe is then used to draw landmarks over the face and track the iris and the eyelids. The position of the iris in the frame is used to as a refernce to use PyAutoGUI to move the cursor and blinking is programmed to click.

## Installation
1. Go To _https://www.python.org/_ and install the latest version of python if not present in the system.
2. Open the CLU and install Mediapipe `py pip install mediapipe`, PyAutoGUI `py pip install pyautogui` and Opencv `py pip install opencv-python`
3. Clone the repositry with `gh repo clone Skanda2007/Eye_Cursor`

## Running
In the CLI open the repositry folder and enter `main.py` or use `py main.py`
