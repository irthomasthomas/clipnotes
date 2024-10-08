import time
import pyperclip

class SelectionStitcher:
    def __init__(self):
        self.state = "IDLE"
        self.first_selection = ""

    def show_notification(self, message):
        print(f"Selection Stitcher: {message}")

    def run(self):
        last_clipboard_content = pyperclip.paste()

        try:
            while True:
                current_clipboard_content = pyperclip.paste()

                if current_clipboard_content != last_clipboard_content:
                    if self.state == "IDLE":
                        self.first_selection = current_clipboard_content
                        self.state = "FIRST_SELECTION_CAPTURED"
                        self.show_notification("First selection captured.")
                    elif self.state == "FIRST_SELECTION_CAPTURED":
                        stitched_selection = f"{self.first_selection} {current_clipboard_content}"
                        pyperclip.copy(stitched_selection)
                        self.state = "IDLE"
                        self.show_notification("Selection stitched and copied to clipboard.")

                    last_clipboard_content = current_clipboard_content

                time.sleep(0.5)
        except KeyboardInterrupt:
            print("Selection Stitcher: Stopped.")

if __name__ == "__main__":
    stitcher = SelectionStitcher()
    stitcher.run()