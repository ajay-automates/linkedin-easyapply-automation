#!/bin/bash
cd "$(dirname "$0")"
echo "Starting LinkedIn Bot..."
python3 linkedin_apply.py
echo ""
echo "Bot finished. Press Enter to close this window."
read
