#!/usr/bin/env python3

import subprocess
import tkinter as tk
from tkinter import simpledialog

def get_clipboard_content():
    try:
        return subprocess.check_output(['xclip', '-o']).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return ""

def set_clipboard_content(text):
    process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
    process.communicate(text.encode('utf-8'))

def main():
    root = tk.Tk()
    root.withdraw()

    subject = get_clipboard_content()
    question = simpledialog.askstring("Question", "Ask a question or add note:")

    if subject and question:
        formatted_text = f"