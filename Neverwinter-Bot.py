import time
import random
import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import pytesseract
import re
import pydirectinput
from PIL import ImageGrab

# Define the target image you're looking for
target_image_path = r'C:\Users\andth\Downloads\python\Characters\cropped_BOURNVITA.png'
target_image = cv2.imread(target_image_path)

# Find the application window by its title
app_window = gw.getWindowsWithTitle('Neverwinter')[0]

# Activate the application window and wait for 2-4 seconds
app_window.activate()
time.sleep(random.uniform(2, 4))

# Get the position and size of the application window
window_x, window_y, window_width, window_height = app_window.left, app_window.top, app_window.width, app_window.height

# Capture the screen within the application window using Pillow (PIL)
screenshot = ImageGrab.grab(bbox=(window_x, window_y, window_x + window_width, window_y + window_height))
screenshot = np.array(screenshot)
screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

# Perform image matching to find the target image
result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
top_left = max_loc
bottom_right = (top_left[0] + target_image.shape[1], top_left[1] + target_image.shape[0])

# Calculate the center of the found image
center_x = (top_left[0] + bottom_right[0]) // 2
center_y = (top_left[1] + bottom_right[1]) // 2

# Move the cursor gradually to the center of the found image
pydirectinput.moveTo(center_x, center_y, duration=random.uniform(0.3, 0.7))

# Wait for 0.5-1.5 seconds before starting the double-click simulation
time.sleep(random.uniform(0.5, 1.5))

# Perform a double-click with slight variations in timing
pydirectinput.mouseDown()
pydirectinput.mouseUp()
time.sleep(random.uniform(0.05, 0.15))  # Small delay between clicks
pydirectinput.mouseDown()
pydirectinput.mouseUp()

# Define a regular expression pattern for "loading"
loading_pattern = re.compile(r'loading', re.IGNORECASE)

# Flag to track if Congratulations is found
congratulations_found = False

# Scan the window for the text "loading"
for _ in range(10):  # Repeat the scan 10 times (adjust as needed)
    screenshot = ImageGrab.grab(bbox=(window_x, window_y, window_x + window_width, window_y + window_height))
    screenshot_text = pytesseract.image_to_string(np.array(screenshot))
    
    if "congratulations" in screenshot_text.lower():
        print("Congratulations found!")
        congratulations_found = True
        break
    
    if loading_pattern.search(screenshot_text):
        print("Loading found...")
    else:
        time.sleep(5)  # Wait for 5 seconds before printing
        print("No loading found...")

        # Simulate pressing "Alt" using pydirectinput
        pydirectinput.keyDown('alt')
        time.sleep(random.uniform(0.1, 0.2))
        pydirectinput.keyUp('alt')
        print("Alt key pressed")

        # Wait for 5 seconds
        time.sleep(5)

        # Simulate pressing "Ctrl + I" using pydirectinput
        pydirectinput.keyDown('ctrl')
        pydirectinput.press('i')
        pydirectinput.keyUp('ctrl')
        time.sleep(random.uniform(0.1, 0.2))
        print("Ctrl + I pressed")
        break

# Simulate pressing the "Esc" key twice with a 5-second gap using pydirectinput
pydirectinput.press('esc')
time.sleep(5)
pydirectinput.press('esc')
time.sleep(5)  # Wait for 5 seconds
print("Esc key pressed twice with 5-second gap")

# Simulate pressing the down button 4 times using pydirectinput
pydirectinput.press(["down"] * 4)
time.sleep(random.uniform(0.1, 0.2))

# Simulate pressing the "Enter" key using pydirectinput
pydirectinput.press("enter")
time.sleep(random.uniform(0.1, 0.2))

# Wait for 2 seconds before pressing the "Tab" key
time.sleep(2)
# Simulate pressing the "Tab" key using pydirectinput
pydirectinput.press("tab")

# Wait for 2 seconds before pressing the "Enter" key again
time.sleep(2)
# Simulate pressing the "Enter" key using pydirectinput
pydirectinput.press("enter")
