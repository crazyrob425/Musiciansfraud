"""
MIDI-Based Composition Module
Generates MIDI files from song structure and provides MIDI export
"""

import os
import random
try:
    import mido
    from mido import Message, MidiFile, MidiTrack, MetaMessage
    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False


class MIDIGenerator:
    """Generate MIDI files from song structure"""
    
    def __init__(self):
        """Initialize MIDI generator"""
        self.available = MIDO_AVAILABLE
        
        # MIDI instrument mappings (General MIDI program numbers)
        self.instrument_midi_map = {
            "Piano": 0,          # Acoustic Grand Piano
            "Guitar": 24,        # Acoustic Guitar (nylon)
            "Bass": 32,          # Acoustic Bass
            "Drums": 0,          # Drums (channel 9)
            "Violin": 40,        # Violin
            "Saxophone": 64,     # Soprano Sax
            "Trumpet": 56,       # Trumpet
            "Synthesizer": 80,   # Lead 1 (square)
            "Strings": 48,       # String Ensemble 1
            "Percussion": 115    # Woodblock
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
        
        # Scale notes (C major)
        self.scale_notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C4 to C5 in MIDI
    
    def generate_midi(self, structure, genre, instruments, output_path):
        """
        Generate MIDI file from song structure
        
        Args:
            structure (dict): Song structure dictionary
            genre (str): Musical genre
            instruments (list): List of instrument names
            output_path (str): Path to save MIDI file
            
        Returns:
            str: Path to generated MIDI file, or None if generation fails
        """
        if not MIDO_AVAILABLE:
            print("MIDI generation requires 'mido' library. Install with: pip install mido")
            return None
        
        try:
            # Create MIDI file
            mid = MidiFile()
            
            # Get tempo
            tempo = self.genre_tempos.get(genre, 120)
            microseconds_per_beat = int(60000000 / tempo)
            
            # Create a track for each instrument
            for instrument in instruments:
                track = self._create_instrument_track(
                    instrument, structure, tempo, microseconds_per_beat
                )
                mid.tracks.append(track)
            
            # Save MIDI file
            mid.save(output_path)
            return output_path
            
        except Exception as e:
            print(f"MIDI generation error: {e}")
            return None
    
    def _create_instrument_track(self, instrument, structure, tempo, microseconds_per_beat):
        """Create a MIDI track for an instrument"""
        track = MidiTrack()
        
        # Set track name
        track.append(MetaMessage('track_name', name=instrument, time=0))
        
        # Set tempo (only needed once, but doesn't hurt to add to each track)
        track.append(MetaMessage('set_tempo', tempo=microseconds_per_beat, time=0))
        
        # Determine channel and program
        if instrument == "Drums":
            channel = 9  # MIDI channel 10 (0-indexed as 9)
            program = 0
        else:
            channel = 0
            program = self.instrument_midi_map.get(instrument, 0)
        
        # Set instrument (program change)
        track.append(Message('program_change', program=program, channel=channel, time=0))
        
        # Generate notes based on structure
        ticks_per_beat = 480  # Standard MIDI resolution
        
        for section in structure.get("sections", []):
            section_duration = section.get("duration", 16)  # in seconds
            section_ticks = int((section_duration * tempo / 60) * ticks_per_beat)
            
            if instrument == "Drums":
                self._add_drum_pattern(track, section_ticks, ticks_per_beat, channel)
            elif instrument == "Bass":
                self._add_bass_pattern(track, section_ticks, ticks_per_beat, channel)
            else:
                self._add_melody_pattern(track, section_ticks, ticks_per_beat, channel)
        
        # Add end of track
        track.append(MetaMessage('end_of_track', time=0))
        
        return track
    
    def _add_drum_pattern(self, track, total_ticks, ticks_per_beat, channel):
        """Add drum pattern to track"""
        # Simple 4/4 drum pattern
        # Kick: 36, Snare: 38, Hi-hat: 42
        kick = 36
        snare = 38
        hihat = 42
        
        current_tick = 0
        beat_count = 0
        
        while current_tick < total_ticks:
            # Hi-hat on every eighth note
            track.append(Message('note_on', note=hihat, velocity=64, time=0, channel=channel))
            track.append(Message('note_off', note=hihat, velocity=64, time=int(ticks_per_beat/4), channel=channel))
            
            # Kick on beats 1 and 3
            if beat_count % 4 == 0 or beat_count % 4 == 2:
                track.append(Message('note_on', note=kick, velocity=100, time=0, channel=channel))
                track.append(Message('note_off', note=kick, velocity=100, time=int(ticks_per_beat/4), channel=channel))
            
            # Snare on beats 2 and 4
            if beat_count % 4 == 1 or beat_count % 4 == 3:
                track.append(Message('note_on', note=snare, velocity=90, time=0, channel=channel))
                track.append(Message('note_off', note=snare, velocity=90, time=int(ticks_per_beat/4), channel=channel))
            
            current_tick += ticks_per_beat / 2
            beat_count += 1
    
    def _add_bass_pattern(self, track, total_ticks, ticks_per_beat, channel):
        """Add bass pattern to track"""
        # Use lower octave notes
        bass_notes = [note - 24 for note in self.scale_notes[:5]]
        
        current_tick = 0
        time_delta = 0
        
        while current_tick < total_ticks:
            note = random.choice(bass_notes)
            duration = int(ticks_per_beat)
            
            track.append(Message('note_on', note=note, velocity=80, time=time_delta, channel=channel))
            track.append(Message('note_off', note=note, velocity=80, time=duration, channel=channel))
            
            current_tick += duration
            time_delta = 0  # Reset delta after first note
    
    def _add_melody_pattern(self, track, total_ticks, ticks_per_beat, channel):
        """Add melody pattern to track"""
        current_tick = 0
        time_delta = 0
        
        while current_tick < total_ticks:
            note = random.choice(self.scale_notes)
            duration = random.choice([int(ticks_per_beat/2), int(ticks_per_beat), int(ticks_per_beat*2)])
            
            track.append(Message('note_on', note=note, velocity=70, time=time_delta, channel=channel))
            track.append(Message('note_off', note=note, velocity=70, time=duration, channel=channel))
            
            current_tick += duration
            time_delta = 0  # Reset delta after first note
    
    def is_available(self):
        """Check if MIDI generation is available"""
        return self.available


if __name__ == "__main__":
    # Test the MIDI generator
    gen = MIDIGenerator()
    
    if gen.is_available():
        test_structure = {
            "total_duration": 60,
            "sections": [
                {"type": "verse", "duration": 16},
                {"type": "chorus", "duration": 16},
                {"type": "verse", "duration": 16},
                {"type": "chorus", "duration": 12}
            ]
        }
        
        output = "/tmp/test_song.mid"
        result = gen.generate_midi(
            structure=test_structure,
            genre="Pop",
            instruments=["Piano", "Drums", "Bass"],
            output_path=output
        )
        
        if result:
            print(f"Generated MIDI file: {result}")
        else:
            print("MIDI generation failed")
    else:
        print("MIDI generation not available. Install mido: pip install mido")
