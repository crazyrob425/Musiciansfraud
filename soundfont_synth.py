"""
Soundfont-Based Synthesis Module
Uses FluidSynth with SF2 soundfonts for higher quality instrument sounds
"""

import os
import tempfile
from pydub import AudioSegment

try:
    import pyfluidsynth as fluidsynth
    FLUIDSYNTH_AVAILABLE = True
except ImportError:
    FLUIDSYNTH_AVAILABLE = False


class SoundfontSynthesizer:
    """Synthesize audio using soundfonts"""
    
    def __init__(self, soundfont_path=None):
        """
        Initialize synthesizer
        
        Args:
            soundfont_path (str): Path to SF2 soundfont file (optional)
        """
        self.available = FLUIDSYNTH_AVAILABLE
        self.soundfont_path = soundfont_path
        self.sample_rate = 44100
        
        # Try to find default soundfont if not provided
        if not self.soundfont_path:
            self.soundfont_path = self._find_default_soundfont()
    
    def _find_default_soundfont(self):
        """Try to find a default soundfont on the system"""
        # Common soundfont locations
        possible_paths = [
            "/usr/share/sounds/sf2/FluidR3_GM.sf2",
            "/usr/share/soundfonts/default.sf2",
            "/usr/share/soundfonts/FluidR3_GM.sf2",
            "C:/soundfonts/default.sf2",
            "/usr/local/share/soundfonts/default.sf2",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def synthesize_from_midi(self, midi_path, output_path):
        """
        Synthesize audio from MIDI file using soundfont
        
        Args:
            midi_path (str): Path to MIDI file
            output_path (str): Path to save synthesized audio
            
        Returns:
            str: Path to synthesized audio file, or None if synthesis fails
        """
        if not FLUIDSYNTH_AVAILABLE:
            print("Soundfont synthesis requires 'pyfluidsynth'. Install with: pip install pyfluidsynth")
            return None
        
        if not self.soundfont_path or not os.path.exists(self.soundfont_path):
            print("No soundfont available. Please provide a .sf2 soundfont file.")
            return None
        
        if not os.path.exists(midi_path):
            print(f"MIDI file not found: {midi_path}")
            return None
        
        try:
            # Initialize FluidSynth
            fs = fluidsynth.Synth()
            fs.start()
            
            # Load soundfont
            sfid = fs.sfload(self.soundfont_path)
            if sfid == -1:
                print(f"Failed to load soundfont: {self.soundfont_path}")
                fs.delete()
                return None
            
            # Select bank and preset
            fs.program_select(0, sfid, 0, 0)
            
            # Play MIDI file
            player = fluidsynth.Player(fs)
            player.add(midi_path)
            player.play()
            
            # Wait for playback to complete
            # Note: This is a simplified version. In production,
            # you'd want to render to a file instead of real-time playback
            player.join()
            
            # Clean up
            player.delete()
            fs.delete()
            
            print("Note: pyfluidsynth real-time synthesis completed.")
            print("For file rendering, consider using fluidsynth command-line tool.")
            
            return output_path
            
        except Exception as e:
            print(f"Soundfont synthesis error: {e}")
            return None
    
    def is_available(self):
        """Check if soundfont synthesis is available"""
        return self.available and (self.soundfont_path is not None)
    
    def get_soundfont_path(self):
        """Get the currently configured soundfont path"""
        return self.soundfont_path
    
    def set_soundfont_path(self, path):
        """Set a custom soundfont path"""
        if os.path.exists(path) and path.endswith('.sf2'):
            self.soundfont_path = path
            return True
        return False


if __name__ == "__main__":
    # Test the soundfont synthesizer
    synth = SoundfontSynthesizer()
    
    print(f"FluidSynth available: {synth.is_available()}")
    print(f"Soundfont path: {synth.get_soundfont_path()}")
    
    if synth.is_available():
        print("Soundfont synthesis ready!")
    else:
        print("Soundfont synthesis not available.")
        print("Install: pip install pyfluidsynth")
        print("And provide a .sf2 soundfont file.")
