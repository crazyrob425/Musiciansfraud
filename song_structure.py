"""
Song Structure Generator Module
Creates editable song structures with sections like chorus, verse, bridge, etc.
"""

import random


class SongStructureGenerator:
    """Generate song structure templates"""
    
    def __init__(self):
        """Initialize the structure generator"""
        # Common song structures by genre
        self.genre_structures = {
            "Pop": {
                "sections": ["intro", "verse", "pre-chorus", "chorus", "verse", "pre-chorus", "chorus", "bridge", "chorus", "outro"],
                "tempo": "120-130 BPM",
                "time_signature": "4/4"
            },
            "Rock": {
                "sections": ["intro", "verse", "chorus", "verse", "chorus", "solo", "bridge", "chorus", "outro"],
                "tempo": "110-140 BPM",
                "time_signature": "4/4"
            },
            "Hip-Hop": {
                "sections": ["intro", "verse", "hook", "verse", "hook", "verse", "hook", "outro"],
                "tempo": "80-100 BPM",
                "time_signature": "4/4"
            },
            "R&B": {
                "sections": ["intro", "verse", "chorus", "verse", "chorus", "bridge", "chorus", "ad-libs", "outro"],
                "tempo": "60-90 BPM",
                "time_signature": "4/4"
            },
            "Country": {
                "sections": ["intro", "verse", "chorus", "verse", "chorus", "instrumental", "bridge", "chorus", "outro"],
                "tempo": "100-120 BPM",
                "time_signature": "4/4"
            },
            "Jazz": {
                "sections": ["intro", "head", "solo-1", "solo-2", "head", "outro"],
                "tempo": "120-180 BPM",
                "time_signature": "4/4"
            },
            "Blues": {
                "sections": ["intro", "verse", "verse", "verse", "solo", "verse", "outro"],
                "tempo": "80-120 BPM",
                "time_signature": "12/8"
            },
            "Electronic": {
                "sections": ["intro", "build", "drop", "breakdown", "build", "drop", "outro"],
                "tempo": "120-140 BPM",
                "time_signature": "4/4"
            },
            "Classical": {
                "sections": ["exposition", "development", "recapitulation", "coda"],
                "tempo": "Variable",
                "time_signature": "Variable"
            },
            "Metal": {
                "sections": ["intro", "verse", "chorus", "verse", "chorus", "breakdown", "solo", "bridge", "chorus", "outro"],
                "tempo": "120-180 BPM",
                "time_signature": "4/4"
            },
            "Folk": {
                "sections": ["intro", "verse", "chorus", "verse", "chorus", "verse", "chorus", "outro"],
                "tempo": "90-120 BPM",
                "time_signature": "4/4"
            },
            "Reggae": {
                "sections": ["intro", "verse", "chorus", "verse", "chorus", "bridge", "chorus", "outro"],
                "tempo": "60-90 BPM",
                "time_signature": "4/4"
            }
        }
    
    def generate(self, genre="Pop", lyrics=""):
        """
        Generate song structure
        
        Args:
            genre: The musical genre
            lyrics: The lyrics to structure
            
        Returns:
            Dictionary containing song structure with keys:
                - genre (str): The musical genre
                - tempo (str): Tempo range in BPM
                - time_signature (str): Time signature (e.g., "4/4")
                - sections (list): List of section dictionaries with:
                    - id (int): Section identifier
                    - type (str): Section type (verse, chorus, etc.)
                    - start_time (float): Start time in seconds
                    - duration (float): Duration in seconds
                    - end_time (float): End time in seconds
                    - content (str): Section content/lyrics
                    - notes (str): User notes for this section
                    - editable (bool): Whether section is editable
                - total_duration (float): Total song duration in seconds
                - hooks (list): List of hook dictionaries with timing info
        """
        # Get genre template or use default
        template = self.genre_structures.get(genre, self.genre_structures["Pop"])
        
        # Parse lyrics to identify sections
        lyrics_sections = self._parse_lyrics(lyrics)
        
        # Build structure
        structure = {
            "genre": genre,
            "tempo": template["tempo"],
            "time_signature": template["time_signature"],
            "sections": []
        }
        
        # Create sections with timing
        current_time = 0.0
        for i, section_type in enumerate(template["sections"]):
            section_duration = self._get_section_duration(section_type)
            
            section = {
                "id": i + 1,
                "type": section_type,
                "start_time": current_time,
                "duration": section_duration,
                "end_time": current_time + section_duration,
                "content": self._get_section_content(section_type, lyrics_sections),
                "notes": "",
                "editable": True
            }
            
            structure["sections"].append(section)
            current_time += section_duration
        
        # Add total duration
        structure["total_duration"] = current_time
        
        # Add hooks and key moments
        structure["hooks"] = self._identify_hooks(structure)
        
        return structure
    
    def _parse_lyrics(self, lyrics):
        """Parse lyrics into sections"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in lyrics.split('\n'):
            if line.startswith('[') and line.endswith(']'):
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = line.strip('[]').lower()
                current_content = []
            elif line.strip():
                current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _get_section_duration(self, section_type):
        """Get typical duration for a section type (in seconds)"""
        durations = {
            "intro": 8.0,
            "verse": 16.0,
            "pre-chorus": 8.0,
            "chorus": 16.0,
            "hook": 16.0,
            "bridge": 16.0,
            "solo": 16.0,
            "breakdown": 8.0,
            "build": 8.0,
            "drop": 16.0,
            "instrumental": 16.0,
            "ad-libs": 8.0,
            "outro": 8.0,
            "head": 32.0,
            "solo-1": 32.0,
            "solo-2": 32.0,
            "exposition": 60.0,
            "development": 90.0,
            "recapitulation": 60.0,
            "coda": 20.0
        }
        return durations.get(section_type, 16.0)
    
    def _get_section_content(self, section_type, lyrics_sections):
        """Get content for a specific section"""
        # Map section types to lyrics sections
        section_map = {
            "verse": "verse",
            "chorus": "chorus",
            "hook": "chorus",
            "bridge": "bridge",
            "pre-chorus": "pre-chorus"
        }
        
        # Try to find matching lyrics
        for key, value in section_map.items():
            if key in section_type.lower():
                # Look for matching section in lyrics
                for lyrics_key, content in lyrics_sections.items():
                    if value in lyrics_key.lower():
                        return content
        
        # Return placeholder for instrumental sections
        if section_type in ["intro", "solo", "instrumental", "outro", "breakdown", "build", "drop"]:
            return f"[Instrumental: {section_type.capitalize()}]"
        
        return f"[{section_type.capitalize()} section]"
    
    def _identify_hooks(self, structure):
        """Identify key hooks and memorable moments"""
        hooks = []
        
        for section in structure["sections"]:
            # Choruses are typically hooks
            if "chorus" in section["type"].lower() or "hook" in section["type"].lower():
                hooks.append({
                    "section_id": section["id"],
                    "time": section["start_time"],
                    "type": "melodic_hook",
                    "description": "Main chorus/hook - most memorable part"
                })
            
            # Bridges often have interesting hooks
            if "bridge" in section["type"].lower():
                hooks.append({
                    "section_id": section["id"],
                    "time": section["start_time"],
                    "type": "transitional_hook",
                    "description": "Bridge - contrasting section"
                })
            
            # Drops in electronic music
            if "drop" in section["type"].lower():
                hooks.append({
                    "section_id": section["id"],
                    "time": section["start_time"],
                    "type": "energy_hook",
                    "description": "Drop - high energy moment"
                })
        
        return hooks


if __name__ == "__main__":
    # Test the structure generator
    gen = SongStructureGenerator()
    
    sample_lyrics = """[Verse 1]
Walking down the street
Feeling the beat
Music in my soul

[Chorus]
Oh we can dance tonight
Everything feels right
Together we shine bright"""
    
    structure = gen.generate(genre="Pop", lyrics=sample_lyrics)
    print(f"Generated structure for {structure['genre']}")
    print(f"Total duration: {structure['total_duration']} seconds")
    print(f"Sections: {len(structure['sections'])}")
