import unittest
    from unittest.mock import patch, MagicMock
    from io import StringIO
    import sys

    # Assuming the refactored code is in a file named selection_stitcher.py
    from selection_stitcher import SelectionStitcher

    class TestSelectionStitcher(unittest.TestCase):

        @patch('tkinter.Tk')
        @patch('tkinter.messagebox.showinfo')
        @patch('pyperclip.paste')
        @patch('pyperclip.copy')
        def test_handle_selection(self, mock_copy, mock_paste, mock_showinfo, mock_tk):
            stitcher = SelectionStitcher()
            
            # Test IDLE state
            mock_paste.return_value = "First"
            stitcher.handle_selection()
            self.assertEqual(stitcher.state, "FIRST_SELECTION_CAPTURED")
            self.assertEqual(stitcher.first_selection, "First")
            mock_showinfo.assert_called_with("Selection Stitcher", "First selection captured.")

            # Test FIRST_SELECTION_CAPTURED state
            mock_paste.return_value = "Second"
            stitcher.handle_selection()
            self.assertEqual(stitcher.state, "IDLE")
            mock_copy.assert_called_with("First Second")
            mock_showinfo.assert_called_with("Selection Stitcher", "Selection stitched and copied to clipboard.")

        @patch('tkinter.Tk')
        def test_setup_hotkey(self, mock_tk):
            stitcher = SelectionStitcher()
            mock_tk.return_value.bind.assert_any_call('<Control-s>', stitcher.handle_selection)
            mock_tk.return_value.bind.assert_any_call('<Control-S>', stitcher.handle_selection)
            mock_tk.return_value.bind.assert_any_call('<Control-q>', stitcher.quit_application)
            mock_tk.return_value.bind.assert_any_call('<Control-Q>', stitcher.quit_application)

        @patch('tkinter.Tk')
        @patch('builtins.print')
        def test_run(self, mock_print, mock_tk):
            stitcher = SelectionStitcher()
            stitcher.run()
            mock_print.assert_called_with("Selection Stitcher is running. Press Ctrl+S to capture/stitch selections. Press Ctrl+Q to quit.")
            mock_tk.return_value.mainloop.assert_called_once()

        @patch('tkinter.Tk')
        @patch('tkinter.messagebox.showinfo')
        @patch('pyperclip.paste')
        def test_handle_selection_error(self, mock_paste, mock_showinfo, mock_tk):
            stitcher = SelectionStitcher()
            mock_paste.side_effect = pyperclip.PyperclipException("Test error")
            stitcher.handle_selection()
            mock_showinfo.assert_called_with("Selection Stitcher", "Error accessing clipboard: Test error")

        @patch('tkinter.Tk')
        def test_quit_application(self, mock_tk):
            stitcher = SelectionStitcher()
            stitcher.quit_application()
            mock_tk.return_value.quit.assert_called_once()

    if __name__ == '__main__':
        unittest.main()