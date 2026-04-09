#!/bin/bash
# ────────────────────────────────────────────────────────────
#  LinkedIn Easy Apply Bot — One-time Setup
#  Run this once before using the bot.
# ────────────────────────────────────────────────────────────

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║   LinkedIn Easy Apply Bot — Setup             ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌  Python 3 not found. Please install it from https://python.org"
    exit 1
fi

echo "✅  Python found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦  Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "🌐  Installing Playwright browser (Chromium)..."
python3 -m playwright install chromium

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  Setup complete!                              ║"
echo "║                                               ║"
echo "║  Next steps:                                  ║"
echo "║  1. Edit config.py with your details          ║"
echo "║  2. Run:  python3 linkedin_apply.py           ║"
echo "╚══════════════════════════════════════════════╝"
echo ""
