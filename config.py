class Config:
    # Sentiment Analysis Configuration
    SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    MAX_LENGTH = 128
    DEVICE = "cpu"
    
    # Music Generation Configuration
    MUSICGEN_MODEL = "facebook/musicgen-small"
    AUDIO_SAMPLE_RATE = 32000
    AUDIO_DURATION = 30  # seconds
    AUDIO_OUTPUT_FORMAT = "wav"
    
    # Audio Processing Configuration
    VOLUME_ADJUSTMENT_FACTOR = 0.7
    NORMALIZATION_ENABLED = True
    
    # File Management
    TEMP_AUDIO_DIR = "temp_audio"
    MAX_TEMP_FILES = 10