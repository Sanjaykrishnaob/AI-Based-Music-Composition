import numpy as np
import soundfile as sf
from scipy import signal
import random

class MusicGenerator:
    """Generate simple audio based on music parameters"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.note_frequencies = {
            'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
            'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
            'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
        }
    
    def generate_tone(self, frequency, duration, volume=0.3):
        """Generate a simple sine wave tone"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        # Add harmonics for richer sound
        wave = np.sin(2 * np.pi * frequency * t) * volume
        wave += np.sin(2 * np.pi * frequency * 2 * t) * volume * 0.3
        wave += np.sin(2 * np.pi * frequency * 3 * t) * volume * 0.1
        
        # Apply envelope
        envelope = np.exp(-t * 2)  # Exponential decay
        wave *= envelope
        
        return wave
    
    def chord_to_frequencies(self, chord_name, key='C'):
        """Convert chord notation to frequencies"""
        # Simplified chord mapping
        chord_patterns = {
            'I': [0, 2, 4],  # Major triad
            'ii': [1, 3, 5], 'iii': [2, 4, 6], 'IV': [3, 5, 7],
            'V': [4, 6, 8], 'vi': [5, 7, 9], 'vii': [6, 8, 10]
        }
        
        scale_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        pattern = chord_patterns.get(chord_name, [0, 2, 4])
        
        frequencies = []
        for interval in pattern:
            note_index = (scale_notes.index(key) + interval) % 7
            note = scale_notes[note_index]
            frequencies.append(self.note_frequencies[note])
        
        return frequencies
    
    def generate_chord_progression(self, parameters, duration=8.0):
        """Generate audio for a chord progression"""
        chord_progression = parameters.get('chord_progression', ['I', 'V', 'vi', 'IV'])
        key = parameters.get('suggested_key', 'C')
        tempo = parameters.get('tempo', 120)
        
        # Calculate chord duration
        chord_duration = duration / len(chord_progression)
        
        audio = np.array([])
        
        for chord in chord_progression:
            frequencies = self.chord_to_frequencies(chord, key)
            chord_audio = np.zeros(int(self.sample_rate * chord_duration))
            
            # Mix frequencies for chord
            for freq in frequencies:
                tone = self.generate_tone(freq, chord_duration, volume=0.2)
                chord_audio += tone[:len(chord_audio)]
            
            audio = np.concatenate([audio, chord_audio])
        
        return audio
    
    def generate_melody(self, parameters, duration=8.0):
        """Generate a simple melody"""
        key = parameters.get('suggested_key', 'C')
        mood = parameters.get('mood_category', 'calm')
        energy = parameters.get('energy_level', 5)
        
        # Adjust note selection based on mood
        if mood == 'happy':
            scale = [0, 2, 4, 5, 7, 9, 11]  # Major scale
        elif mood == 'sad':
            scale = [0, 2, 3, 5, 7, 8, 10]  # Natural minor
        else:
            scale = [0, 2, 4, 5, 7, 9, 11]  # Default to major
        
        note_duration = 0.5  # Half second per note
        num_notes = int(duration / note_duration)
        
        audio = np.array([])
        base_freq = self.note_frequencies[key]
        
        for _ in range(num_notes):
            # Choose random note from scale
            scale_degree = random.choice(scale)
            frequency = base_freq * (2 ** (scale_degree / 12))
            
            # Adjust volume based on energy
            volume = 0.1 + (energy / 10) * 0.2
            
            note = self.generate_tone(frequency, note_duration, volume)
            audio = np.concatenate([audio, note])
        
        return audio
    
    def save_audio(self, audio, filename):
        """Save audio to file"""
        # Normalize audio
        audio = audio / np.max(np.abs(audio))
        sf.write(filename, audio, self.sample_rate)
        return filename
