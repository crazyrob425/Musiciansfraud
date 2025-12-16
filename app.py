"""
AI Song Generator Application
Main entry point for the AI music generation web app
"""

import os
import json
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from lyrics_generator import LyricsGenerator
from song_structure import SongStructureGenerator
from audio_generator import AudioGenerator
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Create output directory for generated songs
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize generators
lyrics_gen = LyricsGenerator()
structure_gen = SongStructureGenerator()
audio_gen = AudioGenerator()

# Available genres
GENRES = [
    "Pop", "Rock", "Hip-Hop", "R&B", "Country", 
    "Jazz", "Blues", "Electronic", "Classical", "Metal",
    "Folk", "Reggae", "Indie", "Alternative", "Soul"
]

# Available instruments
INSTRUMENTS = [
    "Piano", "Guitar", "Bass", "Drums", "Violin",
    "Saxophone", "Trumpet", "Synthesizer", "Strings", "Percussion"
]

# Vocal options
VOCAL_OPTIONS = [
    "Male", "Female", "Mixed", "Choir", "Rap"
]


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', 
                         genres=GENRES,
                         instruments=INSTRUMENTS,
                         vocal_options=VOCAL_OPTIONS)


@app.route('/api/generate-lyrics', methods=['POST'])
def generate_lyrics():
    """Generate lyrics based on user input"""
    try:
        data = request.json
        genre = data.get('genre', 'Pop')
        topic = data.get('topic', 'love')
        
        # Generate lyrics
        lyrics = lyrics_gen.generate(genre=genre, topic=topic)
        
        return jsonify({
            'success': True,
            'lyrics': lyrics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/generate-structure', methods=['POST'])
def generate_structure():
    """Generate song structure"""
    try:
        data = request.json
        genre = data.get('genre', 'Pop')
        lyrics = data.get('lyrics', '')
        
        # Generate structure
        structure = structure_gen.generate(genre=genre, lyrics=lyrics)
        
        return jsonify({
            'success': True,
            'structure': structure
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/generate-audio', methods=['POST'])
def generate_audio():
    """Generate audio from lyrics and structure"""
    try:
        data = request.json
        genre = data.get('genre', 'Pop')
        lyrics = data.get('lyrics', '')
        structure = data.get('structure', {})
        instruments = data.get('instruments', ['Piano', 'Drums'])
        vocal_type = data.get('vocal_type', 'Mixed')
        
        # Generate unique filename
        song_id = str(uuid.uuid4())
        output_path = os.path.join(OUTPUT_DIR, f'{song_id}.mp3')
        
        # Generate audio
        audio_gen.generate(
            lyrics=lyrics,
            structure=structure,
            genre=genre,
            instruments=instruments,
            vocal_type=vocal_type,
            output_path=output_path
        )
        
        return jsonify({
            'success': True,
            'song_id': song_id,
            'download_url': f'/api/download/{song_id}',
            'midi_url': f'/api/download-midi/{song_id}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/download/<song_id>')
def download_song(song_id):
    """Download generated song"""
    try:
        file_path = os.path.join(OUTPUT_DIR, f'{song_id}.mp3')
        if os.path.exists(file_path):
            return send_file(file_path, 
                           as_attachment=True,
                           download_name=f'ai_song_{song_id}.mp3',
                           mimetype='audio/mpeg')
        else:
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/download-midi/<song_id>')
def download_midi(song_id):
    """Download generated MIDI file"""
    try:
        file_path = os.path.join(OUTPUT_DIR, f'{song_id}.mid')
        if os.path.exists(file_path):
            return send_file(file_path, 
                           as_attachment=True,
                           download_name=f'ai_song_{song_id}.mid',
                           mimetype='audio/midi')
        else:
            return jsonify({
                'success': False,
                'error': 'MIDI file not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/save-project', methods=['POST'])
def save_project():
    """Save project state"""
    try:
        data = request.json
        project_id = str(uuid.uuid4())
        project_path = os.path.join(OUTPUT_DIR, f'{project_id}.json')
        
        with open(project_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return jsonify({
            'success': True,
            'project_id': project_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/load-project/<project_id>')
def load_project(project_id):
    """Load project state"""
    try:
        project_path = os.path.join(OUTPUT_DIR, f'{project_id}.json')
        if os.path.exists(project_path):
            with open(project_path, 'r') as f:
                project_data = json.load(f)
            return jsonify({
                'success': True,
                'data': project_data
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Project not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('APP_PORT', 5000))
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    # Only bind to 0.0.0.0 in development, use 127.0.0.1 in production
    host = '0.0.0.0' if debug_mode else '127.0.0.1'
    app.run(host=host, port=port, debug=debug_mode)
