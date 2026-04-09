#!/bin/bash
# LinkedIn Easy Apply Bot Launcher
# This script starts the bot and applies to jobs automatically

cd "$(dirname "$0")"

# Check if session exists, show status
if [ -f "session.json" ]; then
    echo "✅ Session found - will log in automatically"
else
    echo "⚠️  No saved session - you'll need to log in once"
fi

# Run the bot
python3 linkedin_apply.py
