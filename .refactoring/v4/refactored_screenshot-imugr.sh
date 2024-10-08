import pyttsx3
import pyautogui
from datetime import datetime

def screenshot_with_alert():
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set the message to be spoken
    message = "Errors, Errors. Error Message! Function not activated."

    # Speak the message
    engine.say(message)
    engine.runAndWait()

    # Take a screenshot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_filename = f"screenshot_{timestamp}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_filename)

    print(f"Screenshot saved as {screenshot_filename}")

if __name__ == "__main__":
    screenshot_with_alert()