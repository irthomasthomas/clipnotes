#!/bin/bash

# Function to play the alert sound
play_alert_sound() {
    local message="Errors, Errors. Error Message! Function not activated."
    espeak "$message"
}

# Play a sound to alert the user that a screenshot is being taken
play_alert_sound