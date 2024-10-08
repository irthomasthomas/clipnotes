#!/usr/bin/env python3

import subprocess
import pyperclip

def get_primary_selection():
    return subprocess.check_output(['xclip', '-o', '-selection', 'primary']).decode('utf-8').strip()

def fetch_abstract(text):
    result = subprocess.run(['/home/ShellLM/Projects/clipnotes/fetch-abstract.sh'], 
                            input=text.encode('utf-8'), 
                            capture_output=True, 
                            text=True)
    return result.stdout.strip()

def set_clipboard(text):
    pyperclip.copy(text)

def main():
    primary_selection = get_primary_selection()
    abstract = fetch_abstract(primary_selection)
    set_clipboard(abstract)

if __name__ == "__main__":
    main()