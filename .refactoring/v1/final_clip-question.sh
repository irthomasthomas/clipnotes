#!/usr/bin/env python3

import subprocess
import sys

def get_clipboard_content():
    try:
        return subprocess.check_output(['xclip', '-o']).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        print("Error: Failed to get clipboard content.", file=sys.stderr)
        return ""

def prompt_user_input():
    try:
        return subprocess.check_output(['kdialog', '--inputbox', 'Ask a question or add note', 'Question:']).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        print("Error: Failed to get user input.", file=sys.stderr)
        return ""

def set_clipboard_content(content):
    try:
        subprocess.run(['xclip', '-selection', 'clipboard'], input=content.encode('utf-8'), check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to set clipboard content.", file=sys.stderr)

def main():
    subject = get_clipboard_content()
    question = prompt_user_input()

    if subject and question:
        formatted_content = f"