import pyttsx3

def speak_error_message():
    """
    Play a sound to alert the user that a screenshot is being taken.
    """
    engine = pyttsx3.init()
    message = "Errors, Errors. Error Message! Function not activated."
    engine.say(message)
    engine.runAndWait()

if __name__ == "__main__":
    speak_error_message()