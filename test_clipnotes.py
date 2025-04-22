import unittest
import tempfile
import os
import json
import csv
from unittest.mock import patch, MagicMock
import clipnotes
from clipnotes import ClipboardEntry, Encryptor, ClipboardMonitor, EncryptionError, ClipboardAccessError, FileOperationError

class TestClipNotes(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.temp_dir, 'test_output.txt')

    def tearDown(self):
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_clipboard_entry(self):
        entry = ClipboardEntry("Test content", "2023-06-10 12:00:00", "Test Window")
        self.assertEqual(entry.content, "Test content")
        self.assertEqual(entry.timestamp, "2023-06-10 12:00:00")
        self.assertEqual(entry.window_info, "Test Window")

        entry_dict = entry.to_dict()
        self.assertEqual(entry_dict["content"], "Test content")
        self.assertEqual(entry_dict["timestamp"], "2023-06-10 12:00:00")
        self.assertEqual(entry_dict["window_info"], "Test Window")

    def test_encryptor(self):
        encryptor = Encryptor("test_password")
        original_text = "This is a test"
        encrypted_text = encryptor.encrypt(original_text)
        decrypted_text = encryptor.decrypt(encrypted_text)
        self.assertEqual(original_text, decrypted_text)

        with self.assertRaises(EncryptionError):
            encryptor.decrypt("invalid_encrypted_text")

    @patch('clipnotes.pyperclip.paste')
    @patch('clipnotes.get_active_window_info')
    def test_clipboard_monitor(self, mock_window_info, mock_paste):
        mock_window_info.return_value = "Test Window"
        mock_paste.return_value = "Test clipboard content"

        class Args:
            output = self.output_file
            format = 'txt'
            interval = 0.1
            dedup_limit = 10
            separator = '---'
            encrypt = False
            password = None
            include = None
            exclude = None

        monitor = ClipboardMonitor(Args())
        monitor.start()
        import time
        time.sleep(0.2)  # Allow some time for the monitor to run
        monitor.stop()

        with open(self.output_file, 'r') as f:
            content = f.read()
        self.assertIn("Test clipboard content", content)
        self.assertIn("Test Window", content)

    def test_write_to_file_txt(self):
        entry = ClipboardEntry("Test content", "2023-06-10 12:00:00", "Test Window")
        class Args:
            output = self.output_file
            format = 'txt'
            separator = '---'

        clipnotes.write_to_file(self.output_file, entry, Args())

        with open(self.output_file, 'r') as f:
            content = f.read()
        self.assertIn("Test content", content)
        self.assertIn("2023-06-10 12:00:00", content)
        self.assertIn("Test Window", content)

    def test_write_to_file_json(self):
        entry = ClipboardEntry("Test content", "2023-06-10 12:00:00", "Test Window")
        class Args:
            output = self.output_file
            format = 'json'

        clipnotes.write_to_file(self.output_file, entry, Args())

        with open(self.output_file, 'r') as f:
            content = json.load(f)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]["content"], "Test content")
        self.assertEqual(content[0]["timestamp"], "2023-06-10 12:00:00")
        self.assertEqual(content[0]["window_info"], "Test Window")

    def test_write_to_file_csv(self):
        entry = ClipboardEntry("Test content", "2023-06-10 12:00:00", "Test Window")
        class Args:
            output = self.output_file
            format = 'csv'

        clipnotes.write_to_file(self.output_file, entry, Args())

        with open(self.output_file, 'r') as f:
            reader = csv.DictReader(f)
            content = list(reader)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]["content"], "Test content")
        self.assertEqual(content[0]["timestamp"], "2023-06-10 12:00:00")
        self.assertEqual(content[0]["window_info"], "Test Window")

    def test_regex_filtering(self):
        class Args:
            output = self.output_file
            format = 'txt'
            interval = 0.1
            dedup_limit = 10
            separator = '---'
            encrypt = False
            password = None
            include = r'^https?://'
            exclude = r'^file://'

        monitor = ClipboardMonitor(Args())
        self.assertTrue(monitor.should_process_content("https://example.com"))
        self.assertTrue(monitor.should_process_content("http://example.com"))
        self.assertFalse(monitor.should_process_content("ftp://example.com"))
        self.assertFalse(monitor.should_process_content("file:///home/user/document.txt"))

    @patch('clipnotes.pyperclip.paste')
    def test_clipboard_access_error(self, mock_paste):
        mock_paste.side_effect = clipnotes.pyperclip.PyperclipException("Test error")

        class Args:
            output = self.output_file
            format = 'txt'
            interval = 0.1
            dedup_limit = 10
            separator = '---'
            encrypt = False
            password = None
            include = None
            exclude = None

        monitor = ClipboardMonitor(Args())
        with self.assertRaises(ClipboardAccessError):
            monitor.monitor_clipboard()

    def test_file_operation_error(self):
        entry = ClipboardEntry("Test content", "2023-06-10 12:00:00", "Test Window")
        class Args:
            output = '/nonexistent/directory/file.txt'
            format = 'txt'
            separator = '---'

        with self.assertRaises(FileOperationError):
            clipnotes.write_to_file('/nonexistent/directory/file.txt', entry, Args())

if __name__ == '__main__':
    unittest.main()
