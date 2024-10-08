
    import unittest
    from unittest.mock import patch
    import io
    import sys
    from refactored_script import wrap_in_xml, main

    class TestClipQuestion(unittest.TestCase):
        
        def test_wrap_in_xml(self):
            self.assertEqual(wrap_in_xml("test", "content"), "")
        
        @patch('refactored_script.get_selection')
        @patch('refactored_script.ask_question')
        @patch('refactored_script.pyperclip.copy')
        def test_main(self, mock_copy, mock_ask_question, mock_get_selection):
            mock_get_selection.return_value = "Selected Text"
            mock_ask_question.return_value = "User Question"
            
            # Redirect stdout to capture print output
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            main()
            
            sys.stdout = sys.__stdout__  # Reset redirect
            
            expected_result = "\n"
            
            # Check if pyperclip.copy was called with the correct argument
            mock_copy.assert_called_once_with(expected_result)
            
            # Check if the correct output was printed
            expected_output = f"Result copied to clipboard:\n{expected_result}\n"
            self.assertEqual(captured_output.getvalue(), expected_output)

    if __name__ == '__main__':
        unittest.main()
    