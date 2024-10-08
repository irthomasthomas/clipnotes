#!/usr/bin/env bash

set -euo pipefail

# Constants
STATE_FILE="/tmp/selection_stitch_state"
SELECTION_FILE="/tmp/selection_stitch_selection"
IDLE_STATE="IDLE"
FIRST_SELECTION_STATE="FIRST_SELECTION_CAPTURED"

# Function to show notification
show_notification() {
    kdialog --passivepopup "$1" 2
}

# Function to get clipboard content
get_clipboard_content() {
    xclip -o -selection primary
}

# Function to set clipboard content
set_clipboard_content() {
    echo "$1" | xclip -selection clipboard
}

# Initialize state and selection storage if not present
if [[ ! -f "$STATE_FILE" ]]; then
    echo "$IDLE_STATE" > "$STATE_FILE"
    touch "$SELECTION_FILE"
fi

# Read current state
STATE=$(cat "$STATE_FILE")

case $STATE in
    "$IDLE_STATE")
        # Capture the first selection and transition to FIRST_SELECTION_CAPTURED
        get_clipboard_content > "$SELECTION_FILE"
        echo "$FIRST_SELECTION_STATE" > "$STATE_FILE"
        show_notification "First selection captured."
        ;;
    "$FIRST_SELECTION_STATE")
        # Capture the second selection, stitch with the first, copy to clipboard, and transition to IDLE
        FIRST_SELECTION=$(cat "$SELECTION_FILE")
        SECOND_SELECTION=$(get_clipboard_content)
        set_clipboard_content "$FIRST_SELECTION $SECOND_SELECTION"
        echo "$IDLE_STATE" > "$STATE_FILE"
        show_notification "Selection stitched and copied to clipboard."
        ;;
    *)
        # Reset to IDLE state in case of unexpected state
        echo "$IDLE_STATE" > "$STATE_FILE"
        ;;
esac