#!/bin/bash

# Define the error message
ERROR_MESSAGE="Errors, Errors. Error Message! Function not activated."

# Play a sound to alert the user that an error has occurred
if command -v espeak &> /dev/null; then
    espeak "$ERROR_MESSAGE"
else
    echo "Error: espeak is not installed. Please install it to use audio alerts."
    echo "$ERROR_MESSAGE"
fi