#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || venv\Scripts\activate 2>/dev/null

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Run the application
echo "Starting Helix backend..."
python app.py