import pyautogui
import win32gui
import win32con
import pydirectinput
import os
import time
import pygetwindow as gw
import pytesseract
from PIL import Image, ImageGrab
import cv2

def find_window_by_title(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    return hwnd

def find_image_on_window(hwnd, template_path, screenshot_save_path, threshold=0.8):
    if hwnd != 0:
        # Bring the window to the top
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)

        # Wait for 5 seconds
        time.sleep(5)

        # Take a screenshot of the window
        screenshot = pyautogui.screenshot()

        # Open the template image
        template = Image.open(template_path)

        # Perform image recognition
        result = pyautogui.locate(template, screenshot, grayscale=True, confidence=threshold)
        
        if result is not None:
            # Calculate the coordinates of the matched image's region
            x, y, width, height = result
            screenshot_region = screenshot.crop((x, y, x + width, y + height))
            
            # Save the cropped screenshot
            screenshot_region.save(screenshot_save_path)
            print("Cropped screenshot taken!")

            # Simulate a mouse click on the matched position
            target_x, target_y = int(x + width / 2), int(y + height / 2)
            pydirectinput.click(target_x, target_y)
            print("Mouse click simulated at the matched position.")
            return True
        else:
            return False
    else:
        return False

# Specify the title of the third-party window, the path to the image you want to match,
# and where to save the screenshot
window_title = "Neverwinter"
template_path = "screenshot.png"
screenshot_save_path = "screenshot.png"

# Find the window by title
hwnd = find_window_by_title(window_title)

if hwnd != 0:
    # Call the function to find the image on the window, capture a cropped screenshot, and simulate a click
    if find_image_on_window(hwnd, template_path, screenshot_save_path):
        print("Image found on the window! Cropped screenshot taken and mouse click simulated.")

        # Continue with the code to search for target words
        target_words = ['last', 'played']
        target_window_title = 'Neverwinter'
        screenshot_folder = 'screenshots'

        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)

        while True:
            # Find the target window by its title
            target_window = gw.getWindowsWithTitle(target_window_title)
            if len(target_window) == 0:
                print(f"Target window '{target_window_title}' not found.")
                time.sleep(10)  # Wait before trying again
                continue

            target_window = target_window[0]

            # Activate the target window
            target_window.activate()
            time.sleep(2)

            # Capture a screenshot of the target window
            screenshot = pyautogui.screenshot(region=(
                target_window.left,
                target_window.top,
                target_window.width,
                target_window.height
            ))

            found_words = []

            # Extract the text from the screenshot and convert to lowercase
            screenshot_text = pytesseract.image_to_string(screenshot).lower()
            print(screenshot_text)

            # Search for each target word in the extracted text
            for word in target_words:
                if word.lower() in screenshot_text:
                    found_words.append(word)

            # Save the screenshot to the folder
            timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
            screenshot_path = os.path.join(screenshot_folder, f'screenshot_{timestamp}.png')
            screenshot.save(screenshot_path)

            print(f"Screenshot saved: {screenshot_path}")

            # If all target words are found, perform OCR on the last saved screenshot
            if set(found_words) == set(target_words):
                print("Both words found!")

                # Load the image using OpenCV
                image = cv2.imread(screenshot_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Perform OCR on the image to get bounding box coordinates and text
                data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

                # Read target text from a text file
                with open('target_text.txt', 'r', encoding='utf-8') as file:
                    target_text_list = [line.strip() for line in file.readlines() if line.strip()]

                # Create a set to track found target texts
                found_texts = set()

                # Loop through each detected text block
                for i in range(len(data['text'])):
                    text = data['text'][i]
                    x, y, width, height = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

                    for target_text in target_text_list:
                        if target_text in text:
                            found_texts.add(target_text)
                            print(f"Text found: {text}, Bounding Box: ({x}, {y}, {x + width}, {y + height})")

                            # Add additional padding of 70 pixels towards the left and 50 pixels towards the bottom
                            padding_left = 70
                            padding_bottom = 50
                            cropped_x = max(0, x - padding_left)
                            cropped_y = max(0, y)
                            cropped_width = min(image.shape[1] - cropped_x, width + padding_left)
                            cropped_height = min(image.shape[0] - cropped_y, height + padding_bottom)

                            # Crop the text region with added padding
                            cropped_region = image[cropped_y:cropped_y + cropped_height, cropped_x:cropped_x + cropped_width]

                            # Save the cropped region as a separate image in the 'Characters' folder
                            characters_folder = 'Characters'
                            if not os.path.exists(characters_folder):
                                os.makedirs(characters_folder)

                            save_path = os.path.join(characters_folder, f'cropped_{target_text}.png')
                            cv2.imwrite(save_path, cropped_region)

                            print(f"Saved cropped image: {save_path}\n")

                    if len(found_texts) == len(target_text_list):
                        break  # Stop searching when all target texts are found

                if len(found_texts) == len(target_text_list):
                    print("All target texts were found in the image.")
                else:
                    print("Not all target texts were found in the image.")

                break  # Exit the loop after processing the last saved screenshot

            # Wait for a while before taking the next screenshot
            time.sleep(10)  # Adjust the time interval as needed

    else:
        print("Image not found on the window.")
else:
    print("Window not found!")
