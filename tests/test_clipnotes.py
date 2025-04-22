import pytest
from unittest.mock import patch, MagicMock
import unittest
import clipnotes
from io import StringIO
from selection_stitcher import SelectionStitcher

@pytest.fixture
def mock_pyperclip():
    with patch('clipnotes.pyperclip') as mock:
        yield mock

@pytest.fixture
def mock_psutil():
    with patch('clipnotes.psutil') as mock:
        yield mock

def test_get_active_window_info(mock_psutil):
    process_mock = MagicMock()
    process_mock.name.return_value = "test_process"
    process_mock.cwd.return_value = "/test/path"
    process_mock.parent.return_value = None
    mock_psutil.Process.return_value = process_mock

    result = clipnotes.get_active_window_info()
    assert result == "test_process - /test/path"

def test_write_to_file(tmpdir):
    test_file = tmpdir.join("test_output.txt")
    clipnotes.write_to_file(str(test_file), "Test content", "2023-06-10 15:30:45", "Test Window", "---")
    
    content = test_file.read()
    assert "Test content" in content
    assert "2023-06-10 15:30:45" in content
    assert "Test Window" in content
    assert "---" in content

def test_monitor_clipboard(mock_pyperclip, capsys):
    mock_pyperclip.paste.side_effect = ["content1", "content1", KeyboardInterrupt]
    
    args = MagicMock()
    args.output = "test_output.txt"
    args.interval = 0.1
    args.separator = "---"

    with pytest.raises(SystemExit):
        clipnotes.monitor_clipboard(args)

    captured = capsys.readouterr()
    assert "Clipboard monitoring stopped." in captured.out

# Add more tests as needed

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