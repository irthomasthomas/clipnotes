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

def get_clipboard_content():
    """Get content from primary clipboard selection."""
    return subprocess.check_output(["xclip", "-o", "-selection", "primary"]).decode().strip()

def set_clipboard_content(content):
    """Set content to clipboard selection."""
    subprocess.run(["xclip", "-selection", "clipboard"], input=content.encode())

def show_notification(message):
    """Show a notification using kdialog."""
    subprocess.run(["kdialog", "--passivepopup", message, "2"])

def main():
    initialize_files()

    with open(STATE_FILE, 'r') as f:
        state = f.read().strip()

    if state == "IDLE":
        selection = get_clipboard_content()
        with open(SELECTION_FILE, 'w') as f:
            f.write(selection)
        with open(STATE_FILE, 'w') as f:
            f.write("FIRST_SELECTION_CAPTURED")
        show_notification("First selection captured.")

    elif state == "FIRST_SELECTION_CAPTURED":
        with open(SELECTION_FILE, 'r') as f:
            first_selection = f.read().strip()
        second_selection = get_clipboard_content()
        stitched_selection = f"{first_selection} {second_selection}"
        set_clipboard_content(stitched_selection)
        with open(STATE_FILE, 'w') as f:
            f.write("IDLE")
        show_notification("Selection stitched and copied to clipboard.")

    else:
        with open(STATE_FILE, 'w') as f:
            f.write("IDLE")

if __name__ == "__main__":
    main()