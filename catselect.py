
import time
import pyperclip
import tkinter as tk
from tkinter import messagebox
import unittest
from unittest.mock import patch
from io import StringIO
import sys

class SelectionStitcher:
    def __init__(self):
        self.state = "IDLE"
        self.first_selection = ""

    def show_notification(self, message):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Selection Stitcher", message)
        root.destroy()

    def run(self):
        last_clipboard_content = pyperclip.paste()

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

class TestSelectionStitcher(unittest.TestCase):
    @patch('pyperclip.paste')
    @patch('pyperclip.copy')
    @patch('time.sleep')
    @patch('tkinter.messagebox.showinfo')
    def test_selection_stitching(self, mock_showinfo, mock_sleep, mock_copy, mock_paste):
        # Simulate clipboard contents
        mock_paste.side_effect = ["Initial", "First Selection", "Second Selection", KeyboardInterrupt]
        
        stitcher = SelectionStitcher()
        
        # Capture stdout to check for any print statements (if any)
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            stitcher.run()
        except KeyboardInterrupt:
            pass  # Expected to stop the loop

        sys.stdout = sys.__stdout__  # Reset redirect

        # Check if notifications were shown
        self.assertEqual(mock_showinfo.call_count, 2)
        mock_showinfo.assert_any_call("Selection Stitcher", "First selection captured.")
        mock_showinfo.assert_any_call("Selection Stitcher", "Selection stitched and copied to clipboard.")

        # Check if the stitched selection was copied to clipboard
        mock_copy.assert_called_once_with("First Selection Second Selection")

if __name__ == "__main__":
    # Run the main program if executed directly
    stitcher = SelectionStitcher()
    stitcher.run()
