@echo off
REM Startup script for AI Song Generator (Windows)

echo 🎵 AI Song Generator - Musicians Fraud
echo ======================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create output directory
if not exist "output" mkdir output

REM Check for ffmpeg
where ffmpeg >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ⚠️  WARNING: ffmpeg is not installed!
    echo Audio generation requires ffmpeg.
    echo.
    echo Download from: https://ffmpeg.org/download.html
    echo.
)

REM Start the application
echo.
echo Starting Flask application...
echo Open your browser to: http://localhost:5000
echo.
python app.py

pause
