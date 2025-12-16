@echo off
REM Desktop Application Launcher for Windows
REM Double-click this file to start the AI Song Generator

echo 🎵 AI Song Generator - Musicians Fraud
echo ======================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo ❌ Error: Could not create virtual environment.
        echo Please make sure Python 3.8+ is installed.
        echo.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Checking dependencies...
pip install -q -r requirements.txt
pip install -q pywebview

REM Create output directory
if not exist "output" mkdir output

REM Start the desktop application
echo.
echo Starting AI Song Generator...
echo.
python desktop_app.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ❌ Application closed with an error.
    pause
)
