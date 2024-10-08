import time
import pyperclip
import unittest
from unittest.mock import patch
from io import StringIO
import sys

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

class TestSelectionStitcher(unittest.TestCase):
    @patch('pyperclip.paste')
    @patch('pyperclip.copy')
    @patch('time.sleep')
    def test_selection_stitching(self, mock_sleep, mock_copy, mock_paste):
        # Simulate clipboard contents
        mock_paste.side_effect = ["Initial", "First Selection", "Second Selection", KeyboardInterrupt]
        
        stitcher = SelectionStitcher()
        
        # Capture stdout to check for notifications
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            stitcher.run()
        except KeyboardInterrupt:
            pass  # Expected to stop the loop

        sys.stdout = sys.__stdout__  # Reset redirect

        # Check if notifications were printed
        output = captured_output.getvalue()
        self.assertIn("First selection captured.", output)
        self.assertIn("Selection stitched and copied to clipboard.", output)

        # Check if the stitched selection was copied to clipboard
        mock_copy.assert_called_once_with("First Selection Second Selection")

if __name__ == "__main__":
    # Run the main program if executed directly
    stitcher = SelectionStitcher()
    stitcher.run()