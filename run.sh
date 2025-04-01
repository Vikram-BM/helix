#!/bin/bash

# Helix: Combined Run Script for Frontend and Backend

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required commands
if ! command_exists node; then
    echo "Error: Node.js is required but not installed."
    exit 1
fi

if ! command_exists npm; then
    echo "Error: npm is required but not installed."
    exit 1
fi

if ! command_exists python; then
    echo "Error: Python is required but not installed."
    exit 1
fi

# Start backend in a separate terminal
echo "Starting Helix backend..."
gnome-terminal -- bash -c "cd helix/backend && ./run_backend.sh; exec bash" 2>/dev/null || \
xterm -e "cd helix/backend && ./run_backend.sh; exec bash" 2>/dev/null || \
cmd.exe /c start bash -c "cd helix/backend && ./run_backend.sh" 2>/dev/null || \
osascript -e 'tell app "Terminal" to do script "cd $(pwd)/helix/backend && ./run_backend.sh"' 2>/dev/null || \
echo "Could not open a terminal window for the backend. Please run the backend manually in a separate terminal:"
echo "  cd helix/backend && ./run_backend.sh"

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 5

# Start frontend in a separate terminal (except on Windows which will use the current terminal)
echo "Starting Helix frontend..."
gnome-terminal -- bash -c "cd helix/frontend && ./run_frontend.sh; exec bash" 2>/dev/null || \
xterm -e "cd helix/frontend && ./run_frontend.sh; exec bash" 2>/dev/null || \
osascript -e 'tell app "Terminal" to do script "cd $(pwd)/helix/frontend && ./run_frontend.sh"' 2>/dev/null || \
(cd helix/frontend && ./run_frontend.sh)

echo "Helix is now running!"