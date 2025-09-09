import os
import numpy as np
import torch
from pathlib import Path
import tempfile
import warnings
from config import Config

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Import torchaudio with fallback
try:
    import torchaudio
    TORCHAUDIO_AVAILABLE = True
except ImportError:
    TORCHAUDIO_AVAILABLE = False
    print("⚠️ torchaudio not available, using fallback audio processing")

class MusicGenerator:
    """
    Milestone 2: Music Generation Engine with MusicGen Integration
    
    Features:
    1. Working Music Generation Model Integration (MusicGen)
    2. Audio Processing (Tensor to Audio Conversion, Normalization, Format Handling)
    3. Audio Quality Enhancement (Volume adjustment, 30-sec MP3 generation)
    4. Audio Playback Support for Streamlit
    """
    
    def __init__(self):
        self.setup_models()
        self.setup_audio_config()
        self.setup_temp_directory()
    
    def setup_models(self):
        """Initialize MusicGen model from Hugging Face"""
        try:
            print("🔄 Loading MusicGen model from Hugging Face...")
            
            # Try to import audiocraft (MusicGen)
            try:
                from audiocraft.models import MusicGen
                self.musicgen_model = MusicGen.get_pretrained(Config.MUSICGEN_MODEL)
                self.musicgen_available = True
                print(f"✅ MusicGen model '{Config.MUSICGEN_MODEL}' loaded successfully!")
                
            except ImportError:
                print("⚠️ AudioCraft not installed. Using fallback synthesis...")
                self.musicgen_model = None
                self.musicgen_available = False
                
        except Exception as e:
            print(f"❌ Error loading MusicGen: {e}")
            print("🔄 Falling back to basic audio synthesis...")
            self.musicgen_model = None
            self.musicgen_available = False
    
    def setup_audio_config(self):
        """Configure audio processing parameters"""
        self.sample_rate = Config.AUDIO_SAMPLE_RATE
        self.duration = Config.AUDIO_DURATION
        self.volume_factor = Config.VOLUME_ADJUSTMENT_FACTOR
        
        # Note frequencies for fallback synthesis
        self.note_frequencies = {
            'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
            'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
            'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
        }
    
    def setup_temp_directory(self):
        """Setup temporary directory for audio files"""
        self.temp_dir = Path(Config.TEMP_AUDIO_DIR)
        self.temp_dir.mkdir(exist_ok=True)
    
    def generate_music(self, musical_parameters):
        """
        Main music generation function
        Input: Musical parameters from mood analysis
        Output: Generated audio file path
        """
        try:
            print(f"🎵 Generating music with parameters: {musical_parameters.get('mood_category', 'unknown')} mood")
            
            if self.musicgen_available:
                return self.generate_with_musicgen(musical_parameters)
            else:
                return self.generate_with_fallback(musical_parameters)
                
        except Exception as e:
            print(f"❌ Error in music generation: {e}")
            return self.generate_with_fallback(musical_parameters)
    
    def generate_with_musicgen(self, params):
        """
        Generate music using MusicGen model
        
        Process:
        1. Convert musical parameters to text prompt
        2. Generate audio tensor using MusicGen
        3. Process and save audio
        """
        try:
            # Step 1: Create text prompt for MusicGen
            prompt = self.create_musicgen_prompt(params)
            print(f"🎼 MusicGen prompt: '{prompt}'")
            
            # Step 2: Generate audio tensor
            print("🔄 Generating audio with MusicGen...")
            self.musicgen_model.set_generation_params(duration=self.duration)
            
            with torch.no_grad():
                # Generate audio tensor from text prompt
                audio_tensor = self.musicgen_model.generate([prompt])
            
            # Step 3: Audio Processing Pipeline
            return self.process_audio_tensor(audio_tensor, params)
            
        except Exception as e:
            print(f"❌ MusicGen generation failed: {e}")
            return self.generate_with_fallback(params)
    
    def create_musicgen_prompt(self, params):
        """
        Convert musical parameters to MusicGen text prompt
        
        Format: "upbeat happy music with guitar and drums at 120 BPM"
        """
        mood = params.get('mood_category', 'calm')
        energy = params.get('energy_level', 5)
        tempo = params.get('tempo', 120)
        key = params.get('key', 'major')
        instruments = params.get('instruments', ['piano'])
        genre = params.get('genre_style', 'contemporary')
        
        # Build descriptive prompt
        energy_words = {
            1: "very slow", 2: "slow", 3: "gentle", 4: "relaxed", 5: "moderate",
            6: "upbeat", 7: "energetic", 8: "lively", 9: "dynamic", 10: "intense"
        }
        
        energy_desc = energy_words.get(energy, "moderate")
        instruments_str = " and ".join(instruments[:3])  # Limit to 3 instruments
        
        # Create comprehensive prompt
        prompt = f"{energy_desc} {mood} {genre} music with {instruments_str} in {key} key at {tempo} BPM"
        
        return prompt
    
    def process_audio_tensor(self, audio_tensor, params):
        """
        Audio Processing Pipeline:
        Raw AI Audio Tensor → Normalization → Format Conversion → Quality Enhancement → Final Audio File
        """
        try:
            print("🔄 Processing audio tensor...")
            
            # Step 1: Extract audio waveform from tensor
            # MusicGen outputs shape: (batch, channels, samples)
            if len(audio_tensor.shape) == 3:
                audio_waveform = audio_tensor[0]  # Take first batch
            else:
                audio_waveform = audio_tensor
            
            # Step 2: Audio Normalization
            normalized_audio = self.normalize_audio(audio_waveform)
            
            # Step 3: Quality Enhancement
            enhanced_audio = self.enhance_audio_quality(normalized_audio, params)
            
            # Step 4: Format Conversion and Save
            output_path = self.save_audio_file(enhanced_audio, params)
            
            print("✅ Audio processing complete!")
            return output_path
            
        except Exception as e:
            print(f"❌ Audio processing failed: {e}")
            raise
    
    def normalize_audio(self, audio_tensor):
        """
        Audio Normalization: Ensure consistent volume levels
        """
        if Config.NORMALIZATION_ENABLED:
            # Prevent division by zero
            max_val = torch.max(torch.abs(audio_tensor))
            if max_val > 0:
                normalized = audio_tensor / max_val
            else:
                normalized = audio_tensor
                
            # Apply volume adjustment
            normalized = normalized * self.volume_factor
            return normalized
        
        return audio_tensor
    
    def enhance_audio_quality(self, audio_tensor, params):
        """
        Quality Enhancement: Volume adjustment based on energy level
        """
        energy_level = params.get('energy_level', 5)
        
        # Adjust volume based on energy (energy 1-10 maps to volume 0.3-1.0)
        energy_volume = 0.3 + (energy_level / 10) * 0.7
        
        enhanced = audio_tensor * energy_volume
        
        # Ensure we don't clip
        enhanced = torch.clamp(enhanced, -1.0, 1.0)
        
        return enhanced
    
    def save_audio_file(self, audio_tensor, params):
        """
        Save audio as WAV and convert to MP3 (30 seconds)
        """
        try:
            # Generate unique filename
            mood = params.get('mood_category', 'music')
            timestamp = torch.randint(1000, 9999, (1,)).item()
            
            wav_path = self.temp_dir / f"{mood}_{timestamp}.wav"
            mp3_path = self.temp_dir / f"{mood}_{timestamp}.mp3"
            
            # Save as WAV first
            if TORCHAUDIO_AVAILABLE:
                torchaudio.save(str(wav_path), audio_tensor.cpu(), self.sample_rate)
            else:
                # Fallback using soundfile
                import soundfile as sf
                audio_numpy = audio_tensor.cpu().numpy()
                if len(audio_numpy.shape) > 1:
                    audio_numpy = audio_numpy[0]  # Take first channel
                sf.write(str(wav_path), audio_numpy, self.sample_rate)
            
            # Convert to MP3 using pydub
            return self.convert_to_mp3(wav_path, mp3_path)
            
        except Exception as e:
            print(f"❌ Error saving audio: {e}")
            # Return WAV as fallback
            return str(wav_path) if wav_path.exists() else None
    
    def convert_to_mp3(self, wav_path, mp3_path):
        """
        Convert WAV to MP3 using pydub
        """
        try:
            from pydub import AudioSegment
            
            # Load WAV and convert to MP3
            audio = AudioSegment.from_wav(str(wav_path))
            
            # Ensure 30 seconds duration
            if len(audio) > 30000:  # pydub uses milliseconds
                audio = audio[:30000]
            
            # Export as MP3
            audio.export(str(mp3_path), format="mp3", bitrate="192k")
            
            # Clean up WAV file
            if wav_path.exists():
                wav_path.unlink()
            
            print(f"🎵 Audio saved as MP3: {mp3_path}")
            return str(mp3_path)
            
        except ImportError:
            print("⚠️ pydub not available, keeping WAV format")
            return str(wav_path)
        except Exception as e:
            print(f"⚠️ MP3 conversion failed: {e}, keeping WAV")
            return str(wav_path)
    
    def generate_with_fallback(self, params):
        """
        Fallback music generation using basic synthesis
        """
        try:
            print("🔄 Using fallback synthesis...")
            
            # Generate basic music based on parameters
            audio = self.synthesize_basic_music(params)
            
            # Convert to tensor for consistent processing
            audio_tensor = torch.from_numpy(audio).unsqueeze(0).float()
            
            # Process through same pipeline
            return self.process_audio_tensor(audio_tensor, params)
            
        except Exception as e:
            print(f"❌ Fallback generation failed: {e}")
            return None
    
    def synthesize_basic_music(self, params):
        """
        Basic music synthesis for fallback
        """
        mood = params.get('mood_category', 'calm')
        tempo = params.get('tempo', 120)
        energy = params.get('energy_level', 5)
        key = params.get('key', 'major')
        
        # Calculate note duration based on tempo
        beat_duration = 60.0 / tempo  # seconds per beat
        note_duration = beat_duration / 2  # eighth notes
        
        # Generate chord progression
        if key == 'major':
            chord_notes = [261.63, 329.63, 392.00]  # C major chord
        else:
            chord_notes = [261.63, 311.13, 392.00]  # C minor chord
        
        total_samples = int(self.sample_rate * self.duration)
        audio = np.zeros(total_samples)
        
        # Generate simple chord progression
        for i in range(0, total_samples, int(self.sample_rate * note_duration)):
            chord_length = min(int(self.sample_rate * note_duration), total_samples - i)
            
            # Generate chord
            chord_audio = np.zeros(chord_length)
            for freq in chord_notes:
                t = np.linspace(0, note_duration, chord_length, False)
                wave = np.sin(2 * np.pi * freq * t) * 0.2
                # Add envelope
                envelope = np.exp(-t * 2)
                chord_audio += wave * envelope
            
            audio[i:i+chord_length] = chord_audio
        
        return audio
    
    def get_audio_for_streamlit(self, file_path):
        """
        Prepare audio file for Streamlit playback
        Returns audio bytes and MIME type
        """
        try:
            if not file_path or not Path(file_path).exists():
                return None, None
            
            with open(file_path, 'rb') as f:
                audio_bytes = f.read()
            
            # Determine MIME type
            if file_path.endswith('.mp3'):
                mime_type = "audio/mp3"
            elif file_path.endswith('.wav'):
                mime_type = "audio/wav"
            else:
                mime_type = "audio/mpeg"
            
            return audio_bytes, mime_type
            
        except Exception as e:
            print(f"❌ Error preparing audio for Streamlit: {e}")
            return None, None
    
    def cleanup_temp_files(self):
        """
        Clean up temporary audio files
        """
        try:
            import glob
            temp_files = glob.glob(str(self.temp_dir / "*"))
            
            # Keep only the most recent files
            if len(temp_files) > Config.MAX_TEMP_FILES:
                temp_files.sort(key=os.path.getctime)
                files_to_remove = temp_files[:-Config.MAX_TEMP_FILES]
                
                for file_path in files_to_remove:
                    Path(file_path).unlink()
                    
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")
    
    def get_generation_info(self):
        """
        Return information about the music generation setup
        """
        return {
            "musicgen_available": self.musicgen_available,
            "model_name": Config.MUSICGEN_MODEL if self.musicgen_available else "Fallback Synthesis",
            "sample_rate": self.sample_rate,
            "duration": self.duration,
            "output_format": "MP3 (30 seconds)" if self.musicgen_available else "WAV"
        }
