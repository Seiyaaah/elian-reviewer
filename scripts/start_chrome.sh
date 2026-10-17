#!/bin/bash

# Close any previous Chrome instance started with remote debugging
pkill -f "remote-debugging-port=9222" 2>/dev/null

echo "Starting Google Chrome with remote debugging..."

google-chrome \
    --remote-debugging-port=9222 \
    --user-data-dir="$HOME/.config/google-chrome" \
    --profile-directory="Default"