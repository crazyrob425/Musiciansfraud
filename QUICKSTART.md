# AI Song Generator - Quick Start Guide

Welcome to the AI Song Generator! This guide will help you create your first song in minutes.

## Prerequisites

Before you begin, make sure you have:
- Python 3.8 or higher
- ffmpeg (for audio processing)
- A web browser

## Installation (Quick Method)

### On Linux/Mac:
```bash
chmod +x run.sh
./run.sh
```

### On Windows:
```bash
run.bat
```

The script will:
1. Create a virtual environment
2. Install all dependencies
3. Start the application
4. Open your browser to http://localhost:5000

## Manual Installation

If you prefer to install manually:

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the app
python app.py
```

Then open http://localhost:5000 in your browser.

## Creating Your First Song

### Step 1: Choose Genre & Topic
1. Select a genre from the dropdown (e.g., "Pop")
2. Enter a topic for your lyrics (e.g., "dreams", "love", "adventure")
3. Click "Generate Lyrics"

### Step 2: Edit Your Lyrics
1. Review the generated lyrics in the text area
2. Make any edits you want - change words, add lines, etc.
3. Click "Generate Song Structure" when ready

### Step 3: Select Instruments & Vocals
1. Check the instruments you want (Piano, Drums, Bass are selected by default)
2. Choose a vocal type (Male, Female, Mixed, Choir, or Rap)

### Step 4: Review Song Structure
1. Look at the generated song structure
2. Each section shows timing, content, and type (Verse, Chorus, etc.)
3. Add notes to any section if you want specific changes

### Step 5: Generate Your Song
1. Click "🎵 Generate Full Song"
2. Wait 30-60 seconds for generation
3. Listen to your song in the built-in player
4. Download as MP3

## Tips for Best Results

- **Be Specific**: More specific topics generate better lyrics
- **Mix Instruments**: Combine 3-5 instruments for richer sound
- **Edit Freely**: Don't hesitate to modify generated lyrics
- **Save Projects**: Use "Save Project" to continue work later
- **Try Genres**: Experiment with different genres for the same topic

## Available Genres

- **Pop**: Catchy melodies, 120-130 BPM
- **Rock**: Energetic, guitar-driven, 110-140 BPM
- **Hip-Hop**: Rhythmic, beat-focused, 80-100 BPM
- **R&B**: Smooth, soulful, 60-90 BPM
- **Electronic**: Synthetic sounds, 120-140 BPM
- **Jazz**: Complex harmonies, 120-180 BPM
- **Blues**: Emotional, 80-120 BPM
- **Country**: Storytelling, 100-120 BPM
- **Classical**: Orchestral, variable tempo
- **Metal**: Heavy, aggressive, 120-180 BPM
- **Folk**: Acoustic, natural, 90-120 BPM
- **Reggae**: Laid-back, 60-90 BPM
- **Indie/Alternative**: Experimental, 115-120 BPM
- **Soul**: Emotional, powerful vocals, 80 BPM

## Troubleshooting

### "Audio generation failed"
- Make sure ffmpeg is installed
- Check that you have generated lyrics and structure first

### "Cannot access application"
- Check if port 5000 is already in use
- Try changing APP_PORT in .env file

### "Generation takes too long"
- Longer songs (3+ minutes) take more time
- Be patient - generation can take up to 90 seconds

### "No sound in generated MP3"
- Ensure you selected at least one instrument
- Check that ffmpeg is properly installed

## Getting Help

If you encounter issues:
1. Check the terminal/console for error messages
2. Verify all prerequisites are installed
3. Review the README.md for detailed documentation
4. Check the GitHub issues page

## Next Steps

- Experiment with different genre combinations
- Try different vocal types
- Explore the project save/load feature
- Share your creations!

Enjoy creating music! 🎵
