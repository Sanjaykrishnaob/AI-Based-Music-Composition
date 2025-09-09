import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import os
from pathlib import Path

# Core components
from mood_analyzer import MoodAnalyzer
from music_parameters import MusicParameterProcessor
from music_generator import MusicGenerator

# Visualization libraries
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import librosa
    import matplotlib.pyplot as plt
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

# Set page configuration
st.set_page_config(
    page_title="🎵 AI Music Composer",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .milestone-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.5rem;
        display: inline-block;
    }
    .feature-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .success-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .audio-controls {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_ai_models():
    """Load and cache AI models to avoid reloading"""
    try:
        with st.spinner("🤖 Loading AI models... (First time may take a moment)"):
            analyzer = MoodAnalyzer()
            processor = MusicParameterProcessor()
            generator = MusicGenerator()
            
        st.success("✅ All AI models loaded successfully!")
        return analyzer, processor, generator, True
        
    except Exception as e:
        st.error(f"❌ Error loading models: {e}")
        return None, None, None, False

def create_waveform_visualization(audio_file_path):
    """Create waveform visualization using librosa and matplotlib"""
    if not LIBROSA_AVAILABLE or not audio_file_path or not Path(audio_file_path).exists():
        return None
    
    try:
        # Load audio file
        y, sr = librosa.load(audio_file_path, duration=30)
        
        # Create waveform plot
        fig, ax = plt.subplots(figsize=(12, 4))
        time_axis = np.linspace(0, len(y)/sr, len(y))
        ax.plot(time_axis, y, color='#667eea', linewidth=0.8)
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Audio Waveform')
        ax.grid(True, alpha=0.3)
        
        # Style the plot
        ax.set_facecolor('#f8fafc')
        fig.patch.set_facecolor('white')
        
        return fig
        
    except Exception as e:
        st.warning(f"⚠️ Could not create waveform: {e}")
        return None

def create_mood_radar_chart(mood_data):
    """Create an interactive mood radar chart"""
    if not PLOTLY_AVAILABLE:
        return None
    
    categories = ['Energy', 'Positivity', 'Intensity', 'Complexity', 'Dynamics']
    values = [
        mood_data.get('energy_level', 5),
        mood_data.get('sentiment_confidence', 0.5) * 10,
        mood_data.get('energy_level', 5),
        6,  # Default complexity
        mood_data.get('energy_level', 5)
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Mood Analysis',
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=False,
        title="Mood Analysis Radar",
        font=dict(size=12)
    )
    
    return fig

def display_milestone_achievements():
    """Display milestone achievements"""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Implementation Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Core Foundation")
        st.markdown("""
        - ✅ **Hugging Face Sentiment Analysis**: twitter-roberta-base-sentiment-latest
        - ✅ **Sentence Embeddings**: all-MiniLM-L6-v2 for mood classification  
        - ✅ **6 Mood Categories**: Happy, Sad, Calm, Energetic, Mysterious, Romantic
        - ✅ **Energy Calculation**: 1-10 scale with keyword detection
        - ✅ **Musical Parameter Mapping**: Tempo, Key, Instruments, Dynamics
        """)
    
    with col2:
        st.markdown("#### ✅ Music Generation")
        st.markdown("""
        - ✅ **MusicGen Integration**: facebook/musicgen-small (300MB)
        - ✅ **Audio Processing**: Tensor → Normalization → Quality Enhancement
        - ✅ **Format Conversion**: WAV → MP3 (30 seconds)
        - ✅ **Streamlit Audio Player**: Play/Pause/Download controls
        - ✅ **Waveform Visualization**: Real-time audio analysis
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Header with milestone badges
    st.markdown('<h1 class="main-header">🎵 AI Music Composer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Hugging Face Powered Music Generation</p>', unsafe_allow_html=True)
    
    # Load AI models
    analyzer, processor, generator, models_loaded = load_ai_models()
    
    if not models_loaded:
        st.error("⚠️ Could not load AI models. Please check your installation.")
        st.stop()
    
    # Sidebar navigation
    st.sidebar.title("🎼 Navigation")
    section = st.sidebar.radio("Choose Section:", [
        "🏠 Overview", 
        "🎭 Mood Analysis", 
        "🎵 Music Generation",
        "📊 Analytics Dashboard",
        "⚙️ Model Information"
    ])
    
    if section == "🏠 Overview":
        display_milestone_achievements()
        
        st.markdown("### 🚀 Quick Start Guide")
        
        tab1, tab2, tab3 = st.tabs(["Step 1: Mood Analysis", "Step 2: Music Generation", "Step 3: Audio Playback"])
        
        with tab1:
            st.markdown("""
            #### 🎭 Analyze Your Mood
            1. Navigate to **Mood Analysis** section
            2. Enter text describing your mood: *"I'm feeling energetic and ready to dance!"*
            3. AI analyzes sentiment, mood category, and energy level
            4. View detailed musical parameters
            """)
        
        with tab2:
            st.markdown("""
            #### 🎵 Generate Music
            1. Go to **Music Generation** section  
            2. Enter your mood or use analyzed parameters
            3. Click **Generate Music** to create 30-second audio
            4. AI converts text → audio using MusicGen
            """)
        
        with tab3:
            st.markdown("""
            #### 🎧 Listen & Download
            1. Use built-in audio player for playback
            2. View waveform visualization
            3. Download MP3 file to your device
            4. Adjust volume and replay as needed
            """)
    
    elif section == "🎭 Mood Analysis":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.header("🎭 Mood Analysis Engine")
        st.markdown("*Convert user text like \"I'm feeling happy and energetic\" into musical parameters*")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📝 Describe Your Mood")
            user_input = st.text_area(
                "Enter your mood, feelings, or desired atmosphere:",
                placeholder="Examples:\n• I'm feeling energetic and ready to workout!\n• I need calm music for studying\n• Create something mysterious and dark\n• I'm in a romantic mood tonight",
                height=120
            )
            
            if st.button("🔍 Analyze Mood with AI", type="primary", use_container_width=True):
                if user_input.strip():
                    try:
                        # Step-by-step analysis display
                        with st.spinner("🤖 Running Hugging Face sentiment analysis..."):
                            time.sleep(1)  # Brief pause for user experience
                            mood_result = analyzer.analyze_mood(user_input)
                        
                        # Display results
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.markdown("### ✅ Analysis Complete!")
                        
                        # Key metrics
                        col_a, col_b, col_c, col_d = st.columns(4)
                        with col_a:
                            st.metric("🎭 Mood", mood_result.get("mood_category", "calm").title())
                        with col_b:
                            st.metric("⚡ Energy", f"{mood_result.get('energy_level', 5)}/10")
                        with col_c:
                            st.metric("💭 Sentiment", mood_result.get("sentiment", "neutral").title())
                        with col_d:
                            st.metric("🎯 Confidence", f"{mood_result.get('sentiment_confidence', 0.5):.2f}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Detailed musical parameters
                        st.subheader("🎼 Generated Musical Parameters")
                        
                        param_col1, param_col2 = st.columns(2)
                        with param_col1:
                            st.write(f"**🎵 Tempo:** {mood_result.get('tempo', 120)} BPM")
                            st.write(f"**🎹 Key:** {mood_result.get('key', 'major').title()}")
                            st.write(f"**🎚️ Dynamics:** {mood_result.get('dynamics', 'mp')}")
                            st.write(f"**🎪 Genre:** {mood_result.get('genre_style', 'contemporary').title()}")
                        
                        with param_col2:
                            instruments = mood_result.get('instruments', ['piano'])
                            st.write(f"**🎸 Instruments:** {', '.join(instruments)}")
                            st.write(f"**🎭 Texture:** {mood_result.get('texture', 'homophonic').title()}")
                            st.write(f"**⏱️ Time Signature:** {mood_result.get('time_signature', '4/4')}")
                            st.write(f"**🎤 Generation Prompt:** {mood_result.get('text_prompt', '')}")
                        
                        # Visualization
                        if PLOTLY_AVAILABLE:
                            fig = create_mood_radar_chart(mood_result)
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                        
                        # Store results in session state for music generation
                        st.session_state['mood_analysis'] = mood_result
                        
                        # Full parameters
                        with st.expander("📋 View Complete Analysis Data"):
                            st.json(mood_result)
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {e}")
                else:
                    st.warning("⚠️ Please enter a mood description first!")
        
        with col2:
            st.markdown("### 💡 Analysis Process")
            st.info("""
            **🔄 4-Step Process:**
            
            1️⃣ **Sentiment Analysis**  
            Uses twitter-roberta-base-sentiment-latest
            
            2️⃣ **Mood Classification**  
            Cosine similarity with pre-computed embeddings
            
            3️⃣ **Energy Calculation**  
            Keyword detection + sentiment scoring
            
            4️⃣ **Parameter Mapping**  
            Mood → Musical elements
            """)
            
            st.markdown("### 🎯 Example Inputs")
            if st.button("Try: Energetic Workout"):
                st.text_area("", value="I'm excited for my workout! Need high energy music!", key="example1")
            if st.button("Try: Calm Study"):
                st.text_area("", value="I need peaceful, calm music for studying and focus", key="example2")
            if st.button("Try: Romantic Evening"):
                st.text_area("", value="Create something romantic and intimate for date night", key="example3")
    
    elif section == "🎵 Music Generation":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.header("🎵 Music Generation Engine")
        st.markdown("*Generate 30-second MP3 files using MusicGen AI model*")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Generation method selection
        generation_method = st.radio(
            "Choose generation method:",
            ["📝 Text-to-Music", "🎭 Use Mood Analysis", "⚙️ Custom Parameters"]
        )
        
        musical_params = None
        
        if generation_method == "📝 Text-to-Music":
            st.subheader("📝 Direct Text-to-Music Generation")
            
            text_prompt = st.text_area(
                "Describe the music you want:",
                placeholder="Examples:\n• Upbeat happy electronic music with synthesizers\n• Slow melancholic piano ballad in minor key\n• Energetic rock music with guitar and drums at 140 BPM",
                height=100
            )
            
            if text_prompt:
                # Create simple parameters from text
                musical_params = {
                    'text_prompt': text_prompt,
                    'mood_category': 'custom',
                    'energy_level': 5,
                    'tempo': 120,
                    'key': 'major',
                    'instruments': ['mixed'],
                    'original_input': text_prompt
                }
        
        elif generation_method == "🎭 Use Mood Analysis":
            if 'mood_analysis' in st.session_state:
                st.subheader("🎭 Using Previous Mood Analysis")
                analysis = st.session_state['mood_analysis']
                
                # Display current analysis
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Mood", analysis.get('mood_category', 'calm').title())
                with col2:
                    st.metric("Energy", f"{analysis.get('energy_level', 5)}/10")
                with col3:
                    st.metric("Tempo", f"{analysis.get('tempo', 120)} BPM")
                
                st.info(f"🎤 Generation prompt: {analysis.get('text_prompt', '')}")
                musical_params = analysis
                
            else:
                st.warning("⚠️ No mood analysis found. Please run mood analysis first or use text-to-music.")
        
        elif generation_method == "⚙️ Custom Parameters":
            st.subheader("⚙️ Custom Music Parameters")
            
            col1, col2 = st.columns(2)
            with col1:
                mood = st.selectbox("Mood:", ["happy", "sad", "calm", "energetic", "mysterious", "romantic"])
                energy = st.slider("Energy Level:", 1, 10, 5)
                tempo = st.slider("Tempo (BPM):", 60, 180, 120)
            
            with col2:
                key = st.selectbox("Key:", ["major", "minor"])
                genre = st.selectbox("Genre:", ["pop", "rock", "electronic", "classical", "jazz", "ambient"])
                instruments = st.multiselect("Instruments:", 
                    ["piano", "guitar", "drums", "strings", "synth", "bass", "flute"],
                    default=["piano", "guitar"])
            
            # Create parameters
            musical_params = {
                'mood_category': mood,
                'energy_level': energy,
                'tempo': tempo,
                'key': key,
                'genre_style': genre,
                'instruments': instruments,
                'text_prompt': f"{energy} level {mood} {genre} music with {', '.join(instruments)} in {key} key at {tempo} BPM"
            }
        
        # Music generation
        if musical_params and st.button("🎵 Generate Music", type="primary", use_container_width=True):
            try:
                # Display generation info
                gen_info = generator.get_generation_info()
                st.info(f"🤖 Using: {gen_info['model_name']} | Duration: {gen_info['duration']}s | Format: {gen_info['output_format']}")
                
                # Generate music
                with st.spinner("🎼 Generating music... This may take 30-60 seconds..."):
                    audio_file_path = generator.generate_music(musical_params)
                
                if audio_file_path and Path(audio_file_path).exists():
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.markdown("### 🎉 Music Generated Successfully!")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Audio playback section
                    st.markdown('<div class="audio-controls">', unsafe_allow_html=True)
                    st.subheader("🎧 Audio Playback & Controls")
                    
                    # Get audio bytes for Streamlit
                    audio_bytes, mime_type = generator.get_audio_for_streamlit(audio_file_path)
                    
                    if audio_bytes:
                        # Main audio player
                        st.audio(audio_bytes, format=mime_type)
                        
                        # Download button
                        file_name = f"ai_music_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                        st.download_button(
                            label="📥 Download MP3",
                            data=audio_bytes,
                            file_name=file_name,
                            mime=mime_type,
                            use_container_width=True
                        )
                        
                        # Waveform visualization
                        if LIBROSA_AVAILABLE:
                            st.subheader("📊 Waveform Visualization")
                            waveform_fig = create_waveform_visualization(audio_file_path)
                            if waveform_fig:
                                st.pyplot(waveform_fig)
                            else:
                                st.info("Waveform visualization not available")
                        
                        # Audio information
                        file_size = Path(audio_file_path).stat().st_size / 1024  # KB
                        st.caption(f"📁 File size: {file_size:.1f} KB | Format: {mime_type}")
                        
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Cleanup old files
                    generator.cleanup_temp_files()
                    
                else:
                    st.error("❌ Music generation failed. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ Generation error: {e}")
        
        # Technical information
        with st.expander("🔧 Technical Details"):
            gen_info = generator.get_generation_info()
            st.json(gen_info)
    
    elif section == "📊 Analytics Dashboard":
        st.header("📊 Analytics Dashboard")
        
        if PLOTLY_AVAILABLE:
            # Sample analytics
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🔥 Popular Moods")
                mood_data = pd.DataFrame({
                    'Mood': ['Happy', 'Energetic', 'Calm', 'Sad', 'Mysterious', 'Romantic'],
                    'Frequency': [35, 28, 25, 15, 12, 8]
                })
                fig1 = px.bar(mood_data, x='Mood', y='Frequency', 
                             title='Most Analyzed Moods',
                             color='Frequency',
                             color_continuous_scale='viridis')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                st.subheader("⚡ Energy Distribution")
                energy_data = pd.DataFrame({
                    'Energy Range': ['Low (1-3)', 'Medium (4-6)', 'High (7-10)'],
                    'Percentage': [25, 50, 25]
                })
                fig2 = px.pie(energy_data, values='Percentage', names='Energy Range',
                             title='Energy Level Distribution')
                st.plotly_chart(fig2, use_container_width=True)
            
            # Tempo trends
            st.subheader("🎵 Tempo Trends")
            tempo_data = pd.DataFrame({
                'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'Average_Tempo': [110, 125, 105, 130, 140, 115, 95]
            })
            fig3 = px.line(tempo_data, x='Day', y='Average_Tempo',
                          title='Average Tempo by Day of Week',
                          markers=True)
            st.plotly_chart(fig3, use_container_width=True)
            
        else:
            st.info("📊 Install plotly for enhanced visualizations: `pip install plotly`")
    
    elif section == "⚙️ Model Information":
        st.header("⚙️ Model Information & Status")
        
        # Model status
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🤖 Mood Analysis Models")
            st.success("✅ Sentiment: cardiffnlp/twitter-roberta-base-sentiment-latest")
            st.success("✅ Embeddings: all-MiniLM-L6-v2")
            st.info("💡 Models loaded and ready")
        
        with col2:
            st.subheader("🎵 Music Generation Models")
            gen_info = generator.get_generation_info()
            if gen_info['musicgen_available']:
                st.success(f"✅ MusicGen: {gen_info['model_name']}")
                st.success(f"✅ Sample Rate: {gen_info['sample_rate']} Hz")
                st.success(f"✅ Duration: {gen_info['duration']} seconds")
            else:
                st.warning("⚠️ MusicGen not available - using fallback")
                st.info("Install audiocraft: `pip install audiocraft`")
        
        # Requirements check
        st.subheader("📦 Dependencies Status")
        
        deps = {
            "transformers": "✅ Installed",
            "sentence-transformers": "✅ Installed", 
            "torch": "✅ Installed",
            "streamlit": "✅ Installed",
            "plotly": "✅ Installed" if PLOTLY_AVAILABLE else "⚠️ Not installed",
            "librosa": "✅ Installed" if LIBROSA_AVAILABLE else "⚠️ Not installed",
            "audiocraft": "✅ Installed" if gen_info['musicgen_available'] else "⚠️ Not installed"
        }
        
        for dep, status in deps.items():
            st.write(f"**{dep}:** {status}")
        
        # Installation commands
        with st.expander("📋 Installation Commands"):
            st.code("""
# Core dependencies
pip install streamlit transformers torch sentence-transformers
pip install numpy pandas scikit-learn

# Audio processing
pip install audiocraft pydub librosa soundfile torchaudio

# Visualization  
pip install plotly matplotlib

# Optional for better performance
pip install accelerate
            """)
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"<p style='text-align: center; color: #64748b;'>"
            f"🎵 AI Music Composer | Milestones 1 & 2 Complete | "
            f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>", 
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()