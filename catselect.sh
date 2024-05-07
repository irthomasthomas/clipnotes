#!/bin/bash


# Path to store the state and selections
STATE_FILE="/tmp/selection_stitch_state"
SELECTION_FILE="/tmp/selection_stitch_selection"

# Initialize state and selection storage if not present
if [ ! -f "$STATE_FILE" ]; then
    echo "IDLE" > "$STATE_FILE"
    echo "" > "$SELECTION_FILE"
fi

# Read current state
STATE=$(cat "$STATE_FILE")

case $STATE in
    IDLE)
        # Capture the first selection and transition to FIRST_SELECTION_CAPTURED
        xclip -o -selection primary > "$SELECTION_FILE"
        echo "FIRST_SELECTION_CAPTURED" > "$STATE_FILE"
        kdialog --passivepopup "First selection captured." 2
        ;;
    FIRST_SELECTION_CAPTURED)
        # Capture the second selection, stitch with the first, copy to clipboard, and transition to IDLE
        FIRST_SELECTION=$(cat "$SELECTION_FILE")
        SECOND_SELECTION=$(xclip -o -selection primary)
        echo "$FIRST_SELECTION $SECOND_SELECTION" | xclip -selection clipboard
        echo "IDLE" > "$STATE_FILE"
        kdialog --passivepopup "Selection stitched and copied to clipboard." 2
        ;;
    *)
        # Reset to IDLE state in case of unexpected state
        echo "IDLE" > "$STATE_FILE"
        ;;
esac
