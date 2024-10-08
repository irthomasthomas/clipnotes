#!/usr/bin/env python3

import os
import subprocess
import tempfile

# Constants
STATE_FILE = os.path.join(tempfile.gettempdir(), "selection_stitch_state")
SELECTION_FILE = os.path.join(tempfile.gettempdir(), "selection_stitch_selection")

def initialize_files():
    """Initialize state and selection files if they don't exist."""
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'w') as f:
            f.write("IDLE")
    if not os.path.exists(SELECTION_FILE):
        open(SELECTION_FILE, 'w').close()

def read_state():
    """Read the current state from the state file."""
    with open(STATE_FILE, 'r') as f:
        return f.read().strip()

def write_state(state):
    """Write the given state to the state file."""
    with open(STATE_FILE, 'w') as f:
        f.write(state)

def get_clipboard_content():
    """Get the content of the primary selection."""
    return subprocess.check_output(['xclip', '-o', '-selection', 'primary']).decode('utf-8').strip()

def set_clipboard_content(content):
    """Set the content of the clipboard selection."""
    subprocess.run(['xclip', '-selection', 'clipboard'], input=content.encode('utf-8'))

def show_notification(message):
    """Show a notification using kdialog."""
    subprocess.run(['kdialog', '--passivepopup', message, '2'])

def main():
    initialize_files()
    state = read_state()

    if state == "IDLE":
        selection = get_clipboard_content()
        with open(SELECTION_FILE, 'w') as f:
            f.write(selection)
        write_state("FIRST_SELECTION_CAPTURED")
        show_notification("First selection captured.")
    elif state == "FIRST_SELECTION_CAPTURED":
        with open(SELECTION_FILE, 'r') as f:
            first_selection = f.read().strip()
        second_selection = get_clipboard_content()
        stitched_selection = f"{first_selection} {second_selection}"
        set_clipboard_content(stitched_selection)
        write_state("IDLE")
        show_notification("Selection stitched and copied to clipboard.")
    else:
        write_state("IDLE")

if __name__ == "__main__":
    main()