#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run linter
echo "Running linter..."
flake8 .

# Run tests
echo "Running tests..."
python -m unittest discover -v

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed successfully!"
else
    echo "Some tests failed. Please check the output above."
fi

# Deactivate virtual environment
deactivate
