# Screen-Monitor-Python
Screen Monitor with Tkinter and PyAutoGUI
Overview
This Python program provides a simple graphical interface for monitoring a selected region of your screen. When a change occurs in the selected region, the program emits three beeps to alert you. It's a useful utility for keeping track of changes or updates in a specific area of your screen without having to continually check manually.

Requirements
Python 3.x
Tkinter
PyAutoGUI
OpenCV (cv2)
Pillow (PIL)
winsound (Windows-specific)

How to Use
Clone this repository or download the code.
Run main.py to launch the application.
Click on the "Select Area" button. The main window will minimize, and a screenshot will appear.
Click and drag to select a rectangle area on the screenshot.
Once the area is selected, click "Start Monitoring" on the main window that reappears.
If any change occurs within the selected area, you will hear three beeps.
To stop monitoring, click the "Stop Monitoring" button.
