import tkinter as tk
from tkinter import simpledialog
import pyperclip

def get_clipboard_content():
    try:
        return pyperclip.paste()
    except:
        return ""

def ask_question():
    root = tk.Tk()
    root.withdraw()
    return simpledialog.askstring("Question", "Ask a question or add note:")

def wrap_in_xml(tag, text):
    return f"<{tag}>{text}</{tag}>"

def main():
    subject = get_clipboard_content()
    question = ask_question()

    if subject and question:
        wrapped_subject = wrap_in_xml("subject", subject)
        wrapped_question = wrap_in_xml("reader_note", question)
        result = f"{wrapped_subject}\n{wrapped_question}"
        
        pyperclip.copy(result)
        print("Result copied to clipboard:")
        print(result)
    else:
        print("Operation cancelled or no content available.")

if __name__ == "__main__":
    main()