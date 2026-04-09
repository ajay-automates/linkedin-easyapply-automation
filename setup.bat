@echo off
REM ────────────────────────────────────────────────────────────
REM  LinkedIn Easy Apply Bot — One-time Setup (Windows)
REM  Run this once before using the bot.
REM ────────────────────────────────────────────────────────────

echo.
echo ==========================================
echo   LinkedIn Easy Apply Bot - Setup
echo ==========================================
echo.

python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ERROR: Python not found. Install from https://python.org
    pause
    exit /b 1
)

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Installing Playwright browser (Chromium)...
python -m playwright install chromium

echo.
echo ==========================================
echo   Setup complete!
echo.
echo   Next steps:
echo   1. Edit config.py with your details
echo   2. Run:  python linkedin_apply.py
echo ==========================================
echo.
pause
