# Musicians Fraud - AI Song Generator 🎵

A comprehensive AI-powered web application for generating full studio-quality songs with customizable genres, lyrics, instruments, and song structure.

## Features

✨ **Genre Selection** - Choose from 15+ musical genres (Pop, Rock, Hip-Hop, R&B, Country, Jazz, Blues, Electronic, Classical, Metal, Folk, Reggae, Indie, Alternative, Soul)

📝 **AI Lyrics Generation** - Generate lyrics based on your topic and selected genre

✏️ **Editable Lyrics** - Full editing capability for generated lyrics

🎹 **Instrument Selection** - Choose from 10+ instruments (Piano, Guitar, Bass, Drums, Violin, Saxophone, Trumpet, Synthesizer, Strings, Percussion)

🎤 **Vocal Options** - Select vocal type (Male, Female, Mixed, Choir, Rap)

🎼 **Song Structure Editor** - Generate and edit song structure (verses, chorus, bridge, hooks, etc.)

📋 **Section Notes** - Add notes and edits to individual song sections

🎵 **Audio Generation** - Convert everything into real audio

💿 **MP3 Export** - Export studio-quality songs in MP3 format

💾 **Project Saving** - Save and load your song projects

## Technology Stack

- **Backend**: Python Flask
- **Audio Processing**: Pydub, NumPy, SciPy
- **AI Components**: Open-source/template-based generation
- **Frontend**: HTML, CSS, JavaScript
- **Audio Format**: MP3 (320kbps)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- ffmpeg (required for audio processing)

### Install ffmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

### Install Python Dependencies

1. Clone the repository:
```bash
git clone https://github.com/crazyrob425/Musiciansfraud.git
cd Musiciansfraud
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Copy environment configuration:
```bash
cp .env.example .env
```

## Usage

### Starting the Application

1. Activate your virtual environment (if created):
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

### Creating a Song

1. **Select Genre & Topic**
   - Choose your desired musical genre from the dropdown
   - Enter a topic for your lyrics (e.g., "love", "adventure", "dreams")
   - Click "Generate Lyrics"

2. **Edit Lyrics**
   - Review the generated lyrics in the text area
   - Make any edits or changes as desired
   - Click "Generate Song Structure"

3. **Choose Instruments & Vocals**
   - Select instruments you want in your song (can select multiple)
   - Choose your preferred vocal type

4. **Review Song Structure**
   - View the generated song structure with sections
   - Add notes or edit instructions for each section
   - Review timing and duration

5. **Generate Audio**
   - Click "Generate Full Song" to create the audio
   - Wait for processing (may take 30-60 seconds)
   - Listen to your generated song
   - Download as MP3

6. **Save Your Project**
   - Click "Save Project" to save your work
   - You'll receive a Project ID for future reference

## Project Structure

```
Musiciansfraud/
├── app.py                  # Main Flask application
├── lyrics_generator.py     # Lyrics generation module
├── song_structure.py       # Song structure generator
├── audio_generator.py      # Audio synthesis and generation
├── requirements.txt        # Python dependencies
├── .env.example           # Environment configuration template
├── .gitignore             # Git ignore file
├── templates/
│   └── index.html         # Main web interface
├── output/                # Generated songs and projects (auto-created)
└── README.md              # This file
```

## API Endpoints

### POST /api/generate-lyrics
Generate lyrics based on genre and topic.

**Request:**
```json
{
  "genre": "Pop",
  "topic": "love"
}
```

**Response:**
```json
{
  "success": true,
  "lyrics": "Generated lyrics text..."
}
```

### POST /api/generate-structure
Generate song structure from lyrics.

**Request:**
```json
{
  "genre": "Pop",
  "lyrics": "Song lyrics..."
}
```

**Response:**
```json
{
  "success": true,
  "structure": {
    "tempo": "120-130 BPM",
    "sections": [...],
    ...
  }
}
```

### POST /api/generate-audio
Generate audio file from all components.

**Request:**
```json
{
  "genre": "Pop",
  "lyrics": "Song lyrics...",
  "structure": {...},
  "instruments": ["Piano", "Drums"],
  "vocal_type": "Mixed"
}
```

**Response:**
```json
{
  "success": true,
  "song_id": "uuid-string",
  "download_url": "/api/download/uuid-string"
}
```

### GET /api/download/{song_id}
Download generated MP3 file.

### POST /api/save-project
Save project state.

### GET /api/load-project/{project_id}
Load saved project.

## Configuration

Edit the `.env` file to configure:

```env
FLASK_ENV=development
FLASK_DEBUG=True
APP_PORT=5000
```

## Features in Detail

### Lyrics Generation
- Template-based generation with genre-specific patterns
- Customizable themes and topics
- Support for verses, choruses, and bridges
- Rhyme scheme matching for different genres

### Song Structure
- Genre-specific song structures
- Editable sections with timing
- Hook identification
- Tempo and time signature configuration
- Section notes and annotations

### Audio Generation
- Multi-track synthesis
- Instrument-specific waveforms
- Genre-appropriate effects
- Dynamic mixing and normalization
- Studio-quality MP3 export (320kbps)

## Limitations & Future Improvements

Current implementation uses synthesized audio. Future versions could integrate:
- Advanced AI models for more natural lyrics
- Text-to-speech for actual vocals
- MIDI-based composition
- More sophisticated audio synthesis
- Integration with music generation APIs
- Real instrument samples

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms included in the LICENSE file.

## Acknowledgments

- Built with Flask web framework
- Audio processing with Pydub
- Uses open-source Python libraries

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Note**: This application uses synthesized audio and template-based generation. For production use with advanced AI models, you may want to integrate services like:
- Hugging Face Transformers for lyrics
- Music generation APIs for more realistic audio
- Text-to-speech services for vocals 
