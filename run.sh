#!/bin/bash
# Startup script for AI Song Generator

echo "🎵 AI Song Generator - Musicians Fraud"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create output directory
mkdir -p output

# Check for ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo ""
    echo "⚠️  WARNING: ffmpeg is not installed!"
    echo "Audio generation requires ffmpeg."
    echo ""
    echo "Install it with:"
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo ""
fi

# Start the application
echo ""
echo "Starting Flask application..."
echo "Open your browser to: http://localhost:5000"
echo ""
python app.py
