"""
Audio Generator Module
Generates audio from lyrics and structure using open-source tools
"""

import os
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine, Square, Sawtooth
import random


class AudioGenerator:
    """Generate audio using synthesis and procedural generation"""
    
    # Audio mixing constants
    TRACK_VOLUME_REDUCTION = -6  # dB reduction per track to prevent clipping
    RHYTHM_VOLUME_REDUCTION = -10  # dB reduction for rhythm track
    BASS_VOLUME_REDUCTION = -8  # dB reduction for bass track
    MELODY_VOLUME_REDUCTION = -12  # dB reduction for melody tracks
    VOCAL_VOLUME_REDUCTION = -6  # dB reduction for vocal track
    
    def __init__(self):
        """Initialize the audio generator"""
        # Default sample rate
        self.sample_rate = 44100
        
        # Instrument frequency ranges (in Hz)
        self.instrument_ranges = {
            "Piano": (27.5, 4186),
            "Guitar": (82.4, 1318.5),
            "Bass": (41.2, 329.6),
            "Drums": (60, 200),  # Kick drum range
            "Violin": (196, 2637),
            "Saxophone": (138.6, 880),
            "Trumpet": (164.8, 987.8),
            "Synthesizer": (20, 8000),
            "Strings": (65.4, 1046.5),
            "Percussion": (100, 500)
        }
        
        # Genre tempo mappings (BPM)
        self.genre_tempos = {
            "Pop": 120,
            "Rock": 125,
            "Hip-Hop": 90,
            "R&B": 75,
            "Country": 110,
            "Jazz": 140,
            "Blues": 100,
            "Electronic": 128,
            "Classical": 120,
            "Metal": 150,
            "Folk": 100,
            "Reggae": 75,
            "Indie": 115,
            "Alternative": 120,
            "Soul": 80
        }
        
        # Scale notes (C major for simplicity)
        self.scale = [
            261.63,  # C4
            293.66,  # D4
            329.63,  # E4
            349.23,  # F4
            392.00,  # G4
            440.00,  # A4
            493.88,  # B4
            523.25,  # C5
            587.33,  # D5
            659.25,  # E5
        ]
    
    def generate(self, lyrics, structure, genre, instruments, vocal_type, output_path):
        """
        Generate audio from song parameters
        
        Args:
            lyrics (str): Song lyrics text
            structure (dict): Song structure dictionary from SongStructureGenerator
                Should contain 'sections' list and 'total_duration' float
            genre (str): Musical genre name (e.g., "Pop", "Rock")
            instruments (list): List of instrument names to include
            vocal_type (str): Type of vocals ("Male", "Female", "Mixed", "Choir", "Rap")
            output_path (str): Full path where MP3 file should be saved
            
        Returns:
            str: Path to the generated MP3 file
        """
        # Get tempo for genre
        tempo = self.genre_tempos.get(genre, 120)
        beat_duration = 60.0 / tempo * 1000  # Convert to milliseconds
        
        # Create base tracks
        tracks = []
        
        # Generate rhythm track (drums/percussion)
        if "Drums" in instruments or "Percussion" in instruments:
            rhythm_track = self._generate_rhythm_track(structure, tempo)
            tracks.append(rhythm_track)
        
        # Generate bass track
        if "Bass" in instruments:
            bass_track = self._generate_bass_track(structure, tempo)
            tracks.append(bass_track)
        
        # Generate melodic instruments
        for instrument in instruments:
            if instrument in ["Piano", "Guitar", "Synthesizer", "Strings", "Violin"]:
                melody_track = self._generate_melody_track(instrument, structure, tempo)
                tracks.append(melody_track)
        
        # Generate vocal track (placeholder tone for now)
        vocal_track = self._generate_vocal_track(structure, vocal_type, tempo)
        tracks.append(vocal_track)
        
        # Mix all tracks together
        if tracks:
            mixed_audio = tracks[0]
            for track in tracks[1:]:
                # Ensure tracks are the same length
                if len(track) > len(mixed_audio):
                    mixed_audio = mixed_audio + AudioSegment.silent(duration=len(track) - len(mixed_audio))
                elif len(track) < len(mixed_audio):
                    track = track + AudioSegment.silent(duration=len(mixed_audio) - len(track))
                
                # Mix with reduced volume to prevent clipping
                mixed_audio = mixed_audio.overlay(track + self.TRACK_VOLUME_REDUCTION)
        else:
            # Create silent track if no instruments
            mixed_audio = AudioSegment.silent(duration=int(structure.get("total_duration", 180) * 1000))
        
        # Apply effects based on genre
        mixed_audio = self._apply_genre_effects(mixed_audio, genre)
        
        # Normalize audio
        mixed_audio = self._normalize_audio(mixed_audio)
        
        # Export to MP3
        mixed_audio.export(output_path, format="mp3", bitrate="320k")
        
        return output_path
    
    def _generate_rhythm_track(self, structure, tempo):
        """Generate a rhythm/drum track"""
        beat_duration = 60.0 / tempo * 1000  # milliseconds per beat
        
        # Create kick drum pattern (sine wave at low frequency)
        kick = Sine(60).to_audio_segment(duration=100).fade_out(90)
        
        # Create snare (higher frequency with noise-like quality)
        snare = Square(200).to_audio_segment(duration=100).fade_out(90)
        
        # Create hi-hat (very high frequency)
        hihat = Square(800).to_audio_segment(duration=50).fade_out(45)
        
        # Build the drum pattern (4/4 time signature)
        total_duration = structure.get("total_duration", 180) * 1000
        rhythm_track = AudioSegment.silent(duration=0)
        
        current_time = 0
        beat_count = 0
        
        while current_time < total_duration:
            # Kick on beats 1 and 3
            if beat_count % 4 == 0 or beat_count % 4 == 2:
                rhythm_track += kick
            else:
                rhythm_track += AudioSegment.silent(duration=int(beat_duration/4))
            
            # Snare on beats 2 and 4
            if beat_count % 4 == 1 or beat_count % 4 == 3:
                rhythm_track = rhythm_track.overlay(snare, position=current_time)
            
            # Hi-hat on every eighth note
            rhythm_track = rhythm_track.overlay(hihat, position=current_time)
            
            current_time += beat_duration / 4
            beat_count += 1
        
        return rhythm_track + self.RHYTHM_VOLUME_REDUCTION
    
    def _generate_bass_track(self, structure, tempo):
        """Generate a bass track"""
        beat_duration = 60.0 / tempo * 1000
        total_duration = structure.get("total_duration", 180) * 1000
        
        bass_track = AudioSegment.silent(duration=0)
        
        # Use lower frequencies from scale
        bass_notes = [self.scale[i] / 2 for i in range(5)]  # Lower octave
        
        current_time = 0
        while current_time < total_duration:
            # Choose a random bass note from the scale
            note_freq = random.choice(bass_notes)
            note = Sine(note_freq).to_audio_segment(duration=int(beat_duration))
            note = note.fade_in(10).fade_out(10)
            
            bass_track += note
            current_time += beat_duration
        
        return bass_track + self.BASS_VOLUME_REDUCTION
    
    def _generate_melody_track(self, instrument, structure, tempo):
        """Generate a melodic track for an instrument"""
        beat_duration = 60.0 / tempo * 1000
        total_duration = structure.get("total_duration", 180) * 1000
        
        melody_track = AudioSegment.silent(duration=0)
        
        # Choose waveform based on instrument
        if instrument == "Piano":
            wave_generator = Sine
        elif instrument == "Guitar":
            wave_generator = Sawtooth
        elif instrument == "Synthesizer":
            wave_generator = Square
        else:
            wave_generator = Sine
        
        current_time = 0
        while current_time < total_duration:
            # Create a simple melody using scale notes
            note_freq = random.choice(self.scale)
            note_duration = random.choice([beat_duration / 2, beat_duration, beat_duration * 2])
            
            note = wave_generator(note_freq).to_audio_segment(duration=int(note_duration))
            note = note.fade_in(20).fade_out(20)
            
            melody_track += note
            current_time += note_duration
        
        return melody_track + self.MELODY_VOLUME_REDUCTION
    
    def _generate_vocal_track(self, structure, vocal_type, tempo):
        """Generate a vocal track (placeholder with tones)"""
        beat_duration = 60.0 / tempo * 1000
        total_duration = structure.get("total_duration", 180) * 1000
        
        vocal_track = AudioSegment.silent(duration=0)
        
        # Use middle range frequencies for vocals
        vocal_notes = self.scale[2:8]
        
        current_time = 0
        for section in structure.get("sections", []):
            section_duration = section.get("duration", 16) * 1000
            
            # Only generate vocals for verse, chorus, and bridge sections
            if any(s in section["type"].lower() for s in ["verse", "chorus", "bridge", "hook"]):
                section_audio = AudioSegment.silent(duration=0)
                section_time = 0
                
                while section_time < section_duration:
                    note_freq = random.choice(vocal_notes)
                    note_duration = random.choice([beat_duration, beat_duration * 1.5])
                    
                    # Create vocal-like tone
                    note = Sine(note_freq).to_audio_segment(duration=int(note_duration))
                    note = note.fade_in(30).fade_out(30)
                    
                    section_audio += note
                    section_time += note_duration
                
                vocal_track += section_audio[:int(section_duration)]
            else:
                # Silent for instrumental sections
                vocal_track += AudioSegment.silent(duration=int(section_duration))
            
            current_time += section_duration
        
        return vocal_track + self.VOCAL_VOLUME_REDUCTION
    
    def _apply_genre_effects(self, audio, genre):
        """Apply genre-specific effects"""
        # Apply compression (simulated by reducing dynamic range)
        audio = audio.compress_dynamic_range()
        
        # Genre-specific EQ (simplified)
        if genre == "Rock":
            # Boost highs and lows
            audio = audio.low_pass_filter(8000).high_pass_filter(80)
        elif genre == "Hip-Hop":
            # Boost bass
            audio = audio.low_pass_filter(10000).high_pass_filter(60)
        elif genre == "Jazz":
            # More natural tone
            audio = audio.low_pass_filter(12000).high_pass_filter(100)
        elif genre == "Electronic":
            # Wide frequency range
            audio = audio.low_pass_filter(16000).high_pass_filter(40)
        
        return audio
    
    def _normalize_audio(self, audio):
        """Normalize audio to standard level"""
        # Target -3 dB headroom
        return audio.apply_gain(-3 - audio.max_dBFS)


if __name__ == "__main__":
    # Test the audio generator
    gen = AudioGenerator()
    
    test_structure = {
        "total_duration": 60,
        "sections": [
            {"type": "verse", "duration": 16},
            {"type": "chorus", "duration": 16},
            {"type": "verse", "duration": 16},
            {"type": "chorus", "duration": 12}
        ]
    }
    
    output = "/tmp/test_song.mp3"
    gen.generate(
        lyrics="Test lyrics",
        structure=test_structure,
        genre="Pop",
        instruments=["Piano", "Drums", "Bass"],
        vocal_type="Mixed",
        output_path=output
    )
    print(f"Generated test audio: {output}")
