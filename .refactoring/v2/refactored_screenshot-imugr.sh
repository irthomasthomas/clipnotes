#!/bin/bash

# Function to play the alert sound
play_alert_sound() {
    local message="Errors, Errors. Error Message! Function not activated."
    espeak "$message"
}

# Main execution
play_alert_sound