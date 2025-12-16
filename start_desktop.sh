#!/bin/bash
# Desktop Application Launcher for Linux/Mac
# Run this script to start the AI Song Generator in desktop mode

echo "🎵 AI Song Generator - Musicians Fraud"
echo "======================================"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Error: Could not create virtual environment."
        echo "Please make sure Python 3.8+ is installed."
        echo ""
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "Checking dependencies..."
pip install -q -r requirements.txt
pip install -q pywebview

# Create output directory
mkdir -p output

# Start the desktop application
echo ""
echo "Starting AI Song Generator..."
echo ""
python3 desktop_app.py

# Check exit status
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Application closed with an error."
    read -p "Press Enter to exit..."
fi
