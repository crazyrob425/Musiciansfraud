"""
Text-to-Speech Vocals Module
Generates actual vocal tracks from lyrics using TTS engines
"""

import os
import tempfile
from pydub import AudioSegment
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


class TTSVocalsGenerator:
    """Generate vocal tracks using text-to-speech"""
    
    def __init__(self):
        """Initialize TTS engine"""
        self.pyttsx3_engine = None
        if PYTTSX3_AVAILABLE:
            try:
                self.pyttsx3_engine = pyttsx3.init()
            except Exception:
                self.pyttsx3_engine = None
    
    def generate_vocals(self, lyrics, vocal_type="Mixed", tempo=120, output_path=None):
        """
        Generate vocal track from lyrics using TTS
        
        Args:
            lyrics (str): Song lyrics text
            vocal_type (str): Type of vocals (Male, Female, Mixed, Choir, Rap)
            tempo (int): Song tempo in BPM
            output_path (str): Optional path to save the vocal audio
            
        Returns:
            AudioSegment: Generated vocal audio, or None if generation fails
        """
        # Clean lyrics - remove section markers
        clean_lyrics = self._clean_lyrics(lyrics)
        
        if not clean_lyrics.strip():
            return None
        
        # Try pyttsx3 first (offline, faster)
        if self.pyttsx3_engine:
            try:
                return self._generate_with_pyttsx3(clean_lyrics, vocal_type, output_path)
            except Exception as e:
                print(f"pyttsx3 generation failed: {e}")
        
        # Fall back to gTTS (online, higher quality)
        if GTTS_AVAILABLE:
            try:
                return self._generate_with_gtts(clean_lyrics, vocal_type, output_path)
            except Exception as e:
                print(f"gTTS generation failed: {e}")
        
        return None
    
    def _clean_lyrics(self, lyrics):
        """Remove section markers and clean lyrics for TTS"""
        lines = []
        for line in lyrics.split('\n'):
            # Skip section markers like [Verse 1], [Chorus], etc.
            if line.strip().startswith('[') and line.strip().endswith(']'):
                continue
            # Skip instrumental markers
            if '[Instrumental' in line:
                continue
            if line.strip():
                lines.append(line.strip())
        return ' '.join(lines)
    
    def _generate_with_pyttsx3(self, text, vocal_type, output_path=None):
        """Generate vocals using pyttsx3 (offline)"""
        if not self.pyttsx3_engine:
            return None
        
        # Configure voice based on vocal type
        voices = self.pyttsx3_engine.getProperty('voices')
        if voices:
            if vocal_type == "Male" and len(voices) > 0:
                self.pyttsx3_engine.setProperty('voice', voices[0].id)
            elif vocal_type == "Female" and len(voices) > 1:
                self.pyttsx3_engine.setProperty('voice', voices[1].id)
            elif vocal_type == "Rap":
                # Faster rate for rap
                self.pyttsx3_engine.setProperty('rate', 200)
        
        # Generate to temporary file if no output path provided
        if output_path is None:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            output_path = temp_file.name
            temp_file.close()
        
        # Generate speech
        self.pyttsx3_engine.save_to_file(text, output_path)
        self.pyttsx3_engine.runAndWait()
        
        # Load as AudioSegment
        if os.path.exists(output_path):
            audio = AudioSegment.from_file(output_path)
            # Clean up temp file if we created one
            if output_path.endswith('.wav') and 'tmp' in output_path:
                try:
                    os.unlink(output_path)
                except Exception:
                    pass
            return audio
        
        return None
    
    def _generate_with_gtts(self, text, vocal_type, output_path=None):
        """Generate vocals using Google TTS (online)"""
        if not GTTS_AVAILABLE:
            return None
        
        # Configure language and settings based on vocal type
        lang = 'en'
        slow = False
        
        if vocal_type == "Rap":
            # Faster speech for rap
            slow = False
        else:
            # Normal speech
            slow = False
        
        # Generate to temporary file if no output path provided
        if output_path is None:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            output_path = temp_file.name
            temp_file.close()
        
        # Generate speech
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(output_path)
        
        # Load as AudioSegment
        if os.path.exists(output_path):
            audio = AudioSegment.from_file(output_path)
            # Clean up temp file if we created one
            if output_path.endswith('.mp3') and 'tmp' in output_path:
                try:
                    os.unlink(output_path)
                except Exception:
                    pass
            return audio
        
        return None
    
    def get_available_engines(self):
        """Get list of available TTS engines"""
        engines = []
        if PYTTSX3_AVAILABLE and self.pyttsx3_engine:
            engines.append("pyttsx3")
        if GTTS_AVAILABLE:
            engines.append("gtts")
        return engines


if __name__ == "__main__":
    # Test the TTS vocals generator
    gen = TTSVocalsGenerator()
    
    test_lyrics = """
    [Verse 1]
    Walking down the street
    Feeling the beat
    Music in my soul
    
    [Chorus]
    Oh we can dance tonight
    Everything feels right
    Together we shine bright
    """
    
    print(f"Available TTS engines: {gen.get_available_engines()}")
    
    audio = gen.generate_vocals(test_lyrics, vocal_type="Mixed")
    if audio:
        print(f"Generated vocal audio: {len(audio)}ms duration")
    else:
        print("Vocal generation failed")
