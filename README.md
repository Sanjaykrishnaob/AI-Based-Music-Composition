# 🎵 Symphony Muse - AI Music Composition

## Overview
Symphony Muse is a modern, AI-powered music composition tool that analyzes human emotions and generates personalized music parameters. Using state-of-the-art natural language processing and machine learning models from Hugging Face, it bridges the gap between emotional expression and musical creativity.

## ✨ Features
- **🎭 Advanced Mood Analysis**: Intelligent sentiment analysis using Hugging Face transformers
- **🎶 Music Parameter Generation**: Scientifically-backed musical element creation
- **📊 Interactive Visualizations**: Real-time charts and graphs using Plotly
- **🎵 Audio Generation**: Generate and preview chord progressions and melodies
- **⚙️ Customizable Settings**: Adjust energy levels, complexity, and more
- **🎨 Modern UI/UX**: Clean, responsive design with custom CSS styling
- **📈 Analytics Dashboard**: Track popular moods and generation trends

## 🚀Features
- **Real-time Audio Preview**: Generate and play music based on your mood
- **Enhanced Visualizations**: Interactive charts for mood analysis and parameters
- **Analytics Section**: View trends and statistics
- **Improved UI**: Modern design with gradient cards and better navigation
- **Multiple Audio Types**: Choose between chord progressions and melodies

## 🛠️ Technology Stack
- **Frontend**: Streamlit with custom CSS and Plotly visualizations
- **AI Models**: Hugging Face Transformers (Sentiment Analysis & Embeddings)
- **Audio Processing**: NumPy, SciPy, and SoundFile
- **Data Analysis**: Pandas for data manipulation
- **Music Theory**: Custom algorithms based on established musical principles

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start
1. **Clone or download the project**
   ```bash
   cd AI_music_composition
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to the provided URL

## 📁 Project Structure
```
AI_music_composition/
├── app.py                    # Main Streamlit application
├── mood_analyzer.py          # Mood analysis using AI models
├── music_parameters.py       # Music parameter generation
├── music_generator.py        # Audio generation (NEW)
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── models/                 # AI model cache (auto-created)
└── uploads/               # User uploads (if any)
```

## 🎯 How to Use

### 1. Mood Analysis
- Navigate to the "🎭 Mood Analysis" section
- Describe your mood, feelings, or desired atmosphere
- Click "🔍 Analyze Mood" to get detailed analysis with visualizations

### 2. Music Parameters
- Go to "🎶 Music Parameters" section
- Select a mood category or use analyzed mood
- Adjust energy level and complexity in the sidebar
- Generate parameters and preview audio

### 3. Analytics
- Visit "📊 Analytics" to see usage trends
- View popular moods and tempo distributions

## 🎼 Music Theory Integration

The application uses established music theory principles:
- **Scales**: Major, minor, modal scales based on mood
- **Chord Progressions**: Common progressions (I-V-vi-IV, ii-V-I, etc.)
- **Tempo Mapping**: BPM ranges appropriate for different moods
- **Key Selection**: Major/minor tonality based on sentiment
- **Dynamics**: Volume levels mapped to energy
- **Texture**: Monophonic to polyphonic based on complexity

## 🔧 Configuration

### Model Settings (config.py)
```python
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
MAX_LENGTH = 128
DEVICE = "cpu"  # Change to "cuda" if GPU available
```

### Audio Settings
- Sample Rate: 44.1 kHz
- Audio Format: WAV
- Duration: 8 seconds (configurable)

## 🐛 Troubleshooting

### Common Issues
1. **Model loading errors**: Ensure internet connection for first-time model downloads
2. **Audio playback issues**: Check browser audio permissions
3. **Slow performance**: Consider using GPU by changing DEVICE to "cuda" in config.py


## 🚀 Future Enhancements
- [ ] Real-time microphone input for mood detection
- [ ] MIDI file export
- [ ] Integration with music production software
- [ ] User accounts and saved compositions
- [ ] Collaborative mood analysis
- [ ] Mobile app version



---



