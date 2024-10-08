#!/bin/bash

# Define a function to play the alert sound
play_alert_sound() {
    local message="Errors, Errors. Error Message! Function not activated."
    espeak "$message"
}

# Call the function to play the alert sound
play_alert_sound