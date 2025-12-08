"""
Lyrics Generator Module
Uses AI models to generate lyrics based on genre and topic
"""

import os
import random


class LyricsGenerator:
    """Generate lyrics using AI models or template-based approach"""
    
    def __init__(self):
        """Initialize the lyrics generator"""
        # Genre-specific templates and patterns
        self.genre_patterns = {
            "Pop": {
                "themes": ["love", "heartbreak", "dancing", "party", "dreams"],
                "structure": ["verse", "chorus", "verse", "chorus", "bridge", "chorus"],
                "rhyme_scheme": "AABB"
            },
            "Rock": {
                "themes": ["rebellion", "freedom", "passion", "struggle", "power"],
                "structure": ["verse", "chorus", "verse", "chorus", "solo", "bridge", "chorus"],
                "rhyme_scheme": "ABAB"
            },
            "Hip-Hop": {
                "themes": ["success", "struggle", "ambition", "truth", "life"],
                "structure": ["verse", "hook", "verse", "hook", "verse", "hook"],
                "rhyme_scheme": "AABB"
            },
            "R&B": {
                "themes": ["romance", "desire", "emotions", "relationships", "intimacy"],
                "structure": ["verse", "chorus", "verse", "chorus", "bridge", "chorus"],
                "rhyme_scheme": "ABAB"
            },
            "Country": {
                "themes": ["home", "heartache", "simple life", "memories", "nature"],
                "structure": ["verse", "chorus", "verse", "chorus", "bridge", "chorus"],
                "rhyme_scheme": "ABCB"
            },
            "Blues": {
                "themes": ["hardship", "loss", "longing", "pain", "redemption"],
                "structure": ["verse", "verse", "verse"],
                "rhyme_scheme": "AAB"
            },
            "Electronic": {
                "themes": ["energy", "night", "movement", "technology", "future"],
                "structure": ["intro", "build", "drop", "verse", "build", "drop"],
                "rhyme_scheme": "AABB"
            },
            "Folk": {
                "themes": ["stories", "tradition", "nature", "community", "journey"],
                "structure": ["verse", "chorus", "verse", "chorus", "verse", "chorus"],
                "rhyme_scheme": "ABCB"
            }
        }
        
        # Fallback lyrics templates
        self.templates = {
            "verse": [
                "In the {time} when {subject} {action}",
                "I remember {subject} and the way we {action}",
                "Every {time} I think about {subject}",
                "Walking through the {place} with {subject}",
                "When the {time} comes and {subject} {action}"
            ],
            "chorus": [
                "Oh {subject}, you make me {feeling}",
                "We can {action} together, {subject}",
                "{Subject} and {subject}, forever {feeling}",
                "This is our {time}, our {subject}",
                "Can't you see, {subject}, we're meant to be"
            ],
            "bridge": [
                "Maybe {subject} will {action} someday",
                "I never knew that {subject} could {action}",
                "All this time, {subject} has been {action}",
                "Don't let {subject} just {action} away"
            ]
        }
    
    def generate(self, genre="Pop", topic="love"):
        """
        Generate lyrics based on genre and topic
        
        Args:
            genre: The musical genre
            topic: The main topic/theme of the lyrics
            
        Returns:
            String containing generated lyrics
        """
        # Get genre pattern or use default
        pattern = self.genre_patterns.get(genre, self.genre_patterns["Pop"])
        
        # Generate lyrics based on structure
        lyrics_parts = []
        
        # Create verses
        num_verses = pattern["structure"].count("verse")
        for i in range(num_verses):
            verse = self._generate_verse(genre, topic, i + 1)
            lyrics_parts.append(f"[Verse {i + 1}]")
            lyrics_parts.append(verse)
            lyrics_parts.append("")
        
        # Create chorus
        if "chorus" in pattern["structure"] or "hook" in pattern["structure"]:
            chorus = self._generate_chorus(genre, topic)
            lyrics_parts.append("[Chorus]")
            lyrics_parts.append(chorus)
            lyrics_parts.append("")
        
        # Create bridge if in structure
        if "bridge" in pattern["structure"]:
            bridge = self._generate_bridge(genre, topic)
            lyrics_parts.append("[Bridge]")
            lyrics_parts.append(bridge)
            lyrics_parts.append("")
        
        return "\n".join(lyrics_parts)
    
    def _generate_verse(self, genre, topic, verse_num):
        """Generate a verse"""
        lines = []
        templates = self.templates["verse"]
        
        # Generate 4-8 lines for a verse
        num_lines = random.randint(4, 8)
        
        for i in range(num_lines):
            template = random.choice(templates)
            line = self._fill_template(template, topic)
            lines.append(line)
        
        return "\n".join(lines)
    
    def _generate_chorus(self, genre, topic):
        """Generate a chorus"""
        lines = []
        templates = self.templates["chorus"]
        
        # Generate 4-6 lines for a chorus
        num_lines = random.randint(4, 6)
        
        for i in range(num_lines):
            template = random.choice(templates)
            line = self._fill_template(template, topic)
            lines.append(line)
        
        return "\n".join(lines)
    
    def _generate_bridge(self, genre, topic):
        """Generate a bridge"""
        lines = []
        templates = self.templates["bridge"]
        
        # Generate 4 lines for a bridge
        num_lines = 4
        
        for i in range(num_lines):
            template = random.choice(templates)
            line = self._fill_template(template, topic)
            lines.append(line)
        
        return "\n".join(lines)
    
    def _fill_template(self, template, topic):
        """Fill in template with contextual words"""
        # Word pools for different placeholders
        replacements = {
            "{subject}": [topic, "you", "we", "life", "dreams", "hope", "time"],
            "{action}": ["shine", "dance", "sing", "fly", "run", "fall", "rise"],
            "{feeling}": ["alive", "free", "whole", "strong", "new", "real"],
            "{time}": ["night", "morning", "day", "moment", "summer", "winter"],
            "{place}": ["city", "street", "world", "sky", "road", "home"],
            "{Subject}": [topic.capitalize(), "You", "We", "Life", "Dreams"]
        }
        
        result = template
        for placeholder, options in replacements.items():
            if placeholder in result:
                result = result.replace(placeholder, random.choice(options))
        
        return result


if __name__ == "__main__":
    # Test the lyrics generator
    gen = LyricsGenerator()
    lyrics = gen.generate(genre="Pop", topic="love")
    print(lyrics)
