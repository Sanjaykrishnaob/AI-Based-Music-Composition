import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from config import Config
import re

class MoodAnalyzer:
    def __init__(self):
        """Initialize Hugging Face models for mood analysis"""
        self.setup_models()
        self.mood_embeddings = self.create_mood_embeddings()
        self.energy_keywords = self.initialize_energy_keywords()
    
    def setup_models(self):
        """Initialize Hugging Face models with error handling"""
        try:
            print("🔄 Loading Hugging Face models...")
            
            # Sentiment analysis model from Hugging Face
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=Config.SENTIMENT_MODEL,
                device=0 if torch.cuda.is_available() else -1,
                return_all_scores=True
            )
            
            # Sentence embedding model for mood classification
            self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
            
            print("✅ Hugging Face models loaded successfully!")
            
        except Exception as e:
            print(f"⚠️ Error loading models: {e}")
            # Fallback to simpler models
            print("🔄 Loading fallback models...")
            self.sentiment_pipeline = pipeline("sentiment-analysis", return_all_scores=True)
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Fallback models loaded!")
    
    def create_mood_embeddings(self):
        """Pre-compute embeddings for 6 mood categories using sentence transformers"""
        mood_descriptions = {
            "happy": "joyful cheerful upbeat positive energetic bright excited elated",
            "sad": "melancholy sorrowful depressed gloomy downcast dejected mournful",
            "calm": "peaceful tranquil serene relaxed meditative quiet soothing restful",
            "energetic": "dynamic powerful intense vigorous exciting vibrant lively spirited",
            "mysterious": "enigmatic dark atmospheric suspenseful eerie cryptic shadowy unknown",
            "romantic": "loving tender passionate intimate gentle warm affectionate devoted"
        }
        
        print("🔄 Creating mood embeddings...")
        embeddings = {}
        for mood, description in mood_descriptions.items():
            embedding = self.embedding_model.encode(description)
            embeddings[mood] = embedding
            
        print("✅ Mood embeddings created!")
        return embeddings
    
    def initialize_energy_keywords(self):
        """Initialize energy keyword dictionaries for energy level calculation"""
        return {
            "high_energy": [
                "energetic", "excited", "pump", "workout", "dance", "party", "fast", 
                "intense", "powerful", "dynamic", "vigorous", "lively", "explosive",
                "thrilling", "exhilarating", "pumped", "hyped", "electric", "wild"
            ],
            "low_energy": [
                "calm", "peaceful", "sleep", "meditate", "quiet", "soft", "slow",
                "relaxed", "tranquil", "serene", "gentle", "mellow", "subdued",
                "drowsy", "tired", "lazy", "lethargic", "restful", "soothing"
            ]
        }
    
    def analyze_mood(self, user_input):
        """
        Main Analysis Function: Convert user text to musical parameters
        Input: "I need calm music for studying"
        Output: {tempo: 85, key: "major", mood: "calm", energy: 4, ...}
        """
        
        try:
            print(f"🔄 Analyzing: '{user_input}'")
            
            # Step 1: Get sentiment analysis (positive/negative/neutral + confidence)
            sentiment_result = self.get_sentiment_analysis(user_input)
            
            # Step 2: Find closest mood category using similarity matching
            mood_category = self.classify_mood_with_similarity(user_input)
            
            # Step 3: Calculate energy level (1-10 scale)
            energy_level = self.calculate_energy_level(user_input, sentiment_result)
            
            # Step 4: Convert mood + energy + sentiment → musical parameters
            parameters = self.convert_to_musical_parameters(
                mood_category, energy_level, sentiment_result, user_input
            )
            
            print(f"✅ Analysis complete: {mood_category} mood, energy {energy_level}/10")
            return parameters
            
        except Exception as e:
            print(f"❌ Error in mood analysis: {e}")
            return self.get_default_parameters()
    
    def get_sentiment_analysis(self, text):
        """Step 1: Get sentiment with confidence score using Hugging Face"""
        sentiment_scores = self.sentiment_pipeline(text)[0]
        
        # Find the sentiment with highest score
        best_sentiment = max(sentiment_scores, key=lambda x: x['score'])
        
        # Map label to readable format
        label_mapping = {
            'LABEL_0': 'negative',
            'LABEL_1': 'neutral', 
            'LABEL_2': 'positive'
        }
        
        return {
            'sentiment': label_mapping.get(best_sentiment['label'], best_sentiment['label']),
            'confidence': best_sentiment['score'],
            'all_scores': sentiment_scores
        }
    
    def classify_mood_with_similarity(self, user_input):
        """Step 2: Mood classification using cosine similarity with pre-computed embeddings"""
        # Convert user input to numerical vector (embedding)
        input_embedding = self.embedding_model.encode([user_input])
        
        similarities = {}
        # Compare with pre-stored mood embeddings using cosine similarity
        for mood, mood_embedding in self.mood_embeddings.items():
            similarity = cosine_similarity(
                input_embedding.reshape(1, -1),
                mood_embedding.reshape(1, -1)
            )[0][0]
            similarities[mood] = similarity
        
        # Return mood with highest similarity score
        best_mood = max(similarities, key=similarities.get)
        print(f"🎭 Mood similarities: {similarities}")
        return best_mood
    
    def calculate_energy_level(self, text, sentiment_result):
        """
        Step 3: Energy Level Calculation (1-10 scale)
        Logic:
        - Keyword Detection: Count high/low energy words
        - Sentiment Base: Positive sentiment = higher base energy  
        - Keyword Adjustment: Add/subtract based on energy words found
        - Final Calculation: Combine and limit to 1-10 scale
        """
        text_lower = text.lower()
        
        # Keyword Detection: Count energy words
        high_energy_count = sum(1 for word in self.energy_keywords["high_energy"] 
                               if word in text_lower)
        low_energy_count = sum(1 for word in self.energy_keywords["low_energy"] 
                              if word in text_lower)
        
        # Sentiment Base: Convert sentiment to base energy
        sentiment_confidence = sentiment_result['confidence']
        if sentiment_result['sentiment'] == 'positive':
            base_energy = 6 + (sentiment_confidence * 2)  # 6-8 range
        elif sentiment_result['sentiment'] == 'negative':
            base_energy = 4 - (sentiment_confidence * 2)  # 2-4 range  
        else:  # neutral
            base_energy = 5  # middle ground
        
        # Keyword Adjustment: Modify based on energy words
        energy_adjustment = (high_energy_count - low_energy_count) * 1.5
        
        # Final Calculation: Combine and limit to 1-10 scale
        final_energy = max(1, min(10, base_energy + energy_adjustment))
        
        print(f"⚡ Energy calculation: base={base_energy:.1f}, high_words={high_energy_count}, low_words={low_energy_count}, final={final_energy:.1f}")
        
        return int(round(final_energy))
    
    def convert_to_musical_parameters(self, mood_category, energy_level, sentiment_result, original_text):
        """
        Step 4: Map Musical Parameters
        - Mood → Tempo: Happy = 120 BPM, Sad = 70 BPM
        - Sentiment → Key: Positive = Major key, Negative = Minor key
        - Energy Adjustment: Higher energy = faster tempo
        - Mood → Instruments: Happy = piano/guitar/drums, Sad = piano/strings/cello
        """
        
        # Base tempo mapping by mood
        tempo_mapping = {
            "happy": 120, "sad": 70, "calm": 80,
            "energetic": 140, "mysterious": 90, "romantic": 85
        }
        
        # Key preference based on sentiment
        if sentiment_result['sentiment'] == 'positive':
            key_preference = "major"
        elif sentiment_result['sentiment'] == 'negative':
            key_preference = "minor"
        else:
            key_preference = "major"  # default neutral to major
        
        # Special cases for certain moods
        if mood_category in ["mysterious", "sad"]:
            key_preference = "minor"
        
        # Instrument selection based on mood
        instrument_mapping = {
            "happy": ["piano", "guitar", "drums", "brass"],
            "sad": ["piano", "strings", "cello", "violin"],
            "calm": ["piano", "flute", "soft_strings", "harp"],
            "energetic": ["electric_guitar", "drums", "bass", "synth"],
            "mysterious": ["synth", "dark_strings", "ambient_pad", "low_brass"],
            "romantic": ["piano", "violin", "soft_guitar", "strings"]
        }
        
        # Calculate final tempo with energy adjustment
        base_tempo = tempo_mapping.get(mood_category, 120)
        tempo_adjustment = (energy_level - 5) * 8  # ±8 BPM per energy point
        final_tempo = int(base_tempo + tempo_adjustment)
        
        # Ensure tempo stays in reasonable range
        final_tempo = max(60, min(180, final_tempo))
        
        # Generate comprehensive parameters
        parameters = {
            # Core Analysis Results
            "mood_category": mood_category,
            "energy_level": energy_level,
            "sentiment": sentiment_result['sentiment'],
            "sentiment_confidence": round(sentiment_result['confidence'], 3),
            
            # Musical Elements  
            "tempo": final_tempo,
            "key": key_preference,
            "instruments": instrument_mapping.get(mood_category, ["piano", "strings"]),
            "time_signature": "4/4",
            
            # Advanced Parameters
            "genre_style": self.determine_genre_style(mood_category, energy_level),
            "dynamics": self.map_energy_to_dynamics(energy_level),
            "texture": self.determine_texture(energy_level),
            
            # Generation Hints for AI Model
            "text_prompt": self.create_generation_prompt(mood_category, energy_level, key_preference),
            "original_input": original_text
        }
        
        return parameters
    
    def determine_genre_style(self, mood, energy):
        """Determine genre based on mood and energy with more nuanced mapping"""
        if mood == "energetic":
            if energy >= 8:
                return "electronic_dance"
            elif energy >= 6:
                return "rock"
            else:
                return "pop"
        elif mood == "calm":
            if energy <= 3:
                return "ambient"
            elif energy <= 5:
                return "classical"
            else:
                return "folk"
        elif mood == "sad":
            if energy <= 4:
                return "blues"
            else:
                return "indie"
        elif mood == "happy":
            if energy >= 7:
                return "pop_dance"
            else:
                return "acoustic_pop"
        elif mood == "mysterious":
            return "cinematic"
        elif mood == "romantic":
            return "ballad"
        else:
            return "contemporary"
    
    def map_energy_to_dynamics(self, energy):
        """Map energy level to musical dynamics"""
        if energy <= 2: return "pp"  # pianissimo (very soft)
        elif energy <= 4: return "p"   # piano (soft)
        elif energy <= 6: return "mp"  # mezzo-piano (medium soft)
        elif energy <= 8: return "mf"  # mezzo-forte (medium loud)
        else: return "f"               # forte (loud)
    
    def determine_texture(self, energy):
        """Determine musical texture based on energy"""
        if energy <= 3: return "monophonic"     # single melody line
        elif energy <= 6: return "homophonic"   # melody with accompaniment
        else: return "polyphonic"               # multiple independent melodies
    
    def create_generation_prompt(self, mood, energy, key):
        """Create text prompt for music generation AI models"""
        energy_descriptors = {
            1: "very slow and quiet", 2: "slow and gentle", 3: "calm and peaceful",
            4: "relaxed", 5: "moderate", 6: "moderately energetic", 
            7: "upbeat", 8: "energetic", 9: "very energetic", 10: "intense and powerful"
        }
        
        mood_descriptors = {
            "happy": "joyful and bright",
            "sad": "melancholic and emotional", 
            "calm": "peaceful and serene",
            "energetic": "dynamic and powerful",
            "mysterious": "dark and atmospheric",
            "romantic": "tender and loving"
        }
        
        energy_desc = energy_descriptors.get(energy, "moderate")
        mood_desc = mood_descriptors.get(mood, "pleasant")
        
        return f"{energy_desc} {mood_desc} music in {key} key"
    
    def get_default_parameters(self):
        """Default parameters for fallback scenarios"""
        return {
            "mood_category": "calm",
            "energy_level": 5,
            "sentiment": "neutral",
            "sentiment_confidence": 0.5,
            "tempo": 120,
            "key": "major",
            "instruments": ["piano", "strings"],
            "time_signature": "4/4",
            "genre_style": "contemporary",
            "dynamics": "mp",
            "texture": "homophonic",
            "text_prompt": "moderate peaceful music in major key",
            "original_input": "default"
        }