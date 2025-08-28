import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from mood_analyzer import MoodAnalyzer
from music_parameters import MusicParameterProcessor
import os

# Try to import music generator
try:
    from music_generator import MusicGenerator
    MUSIC_GENERATOR_AVAILABLE = True
except ImportError:
    MUSIC_GENERATOR_AVAILABLE = False

# Try to import plotly, use fallback if not available
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Set page configuration
st.set_page_config(
    page_title="Symphony Muse",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .mood-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .parameter-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def create_mood_visualization(mood_data):
    """Create an interactive mood visualization"""
    if not PLOTLY_AVAILABLE:
        # Fallback to simple bar chart
        if isinstance(mood_data, dict):
            categories = ['Energy', 'Positivity', 'Intensity', 'Complexity']
            values = [
                mood_data.get('energy_level', 5),
                mood_data.get('sentiment_confidence', 0.5) * 10,
                mood_data.get('energy_level', 5),
                5  # Default complexity
            ]
            
            df = pd.DataFrame({
                'Category': categories,
                'Value': values
            })
            st.bar_chart(df.set_index('Category'))
            return None
    
    if isinstance(mood_data, dict):
        # Create a radar chart for mood analysis
        categories = ['Energy', 'Positivity', 'Intensity', 'Complexity']
        values = [
            mood_data.get('energy_level', 5),
            mood_data.get('sentiment_confidence', 0.5) * 10,
            mood_data.get('energy_level', 5),
            5  # Default complexity
        ]
        
        df = pd.DataFrame({
            'Category': categories,
            'Value': values
        })
        
        fig = px.bar(df, x='Category', y='Value', 
                    title='Mood Analysis Results',
                    color='Value',
                    color_continuous_scale='viridis')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        return fig
    return None

def create_parameter_visualization(parameters):
    """Create visualization for music parameters"""
    if not PLOTLY_AVAILABLE:
        # Fallback to simple display
        if isinstance(parameters, dict):
            instruments = parameters.get('instruments', ['piano'])
            st.write("**Instruments:**", ", ".join(instruments))
            return None
    
    if isinstance(parameters, dict):
        # Create a pie chart for instruments
        instruments = parameters.get('instruments', ['piano'])
        instrument_data = pd.DataFrame({
            'Instrument': instruments,
            'Weight': [1] * len(instruments)
        })
        
        fig = px.pie(instrument_data, values='Weight', names='Instrument',
                    title='Instrument Distribution')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        return fig
    return None

@st.cache_resource
def load_models():
    """Cache models to avoid reloading"""
    analyzer = MoodAnalyzer()
    processor = MusicParameterProcessor()
    if MUSIC_GENERATOR_AVAILABLE:
        generator = MusicGenerator()
        return analyzer, processor, generator
    else:
        return analyzer, processor, None

def main():
    # Main header with custom styling
    st.markdown('<h1 class="main-header">🎵 Symphony Muse</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Music Composition & Mood Analysis</p>', unsafe_allow_html=True)

    # Load models once
    with st.spinner("🤖 Loading AI models... (First time may take a moment)"):
        analyzer, processor, generator = load_models()

    # Enhanced sidebar with more options
    st.sidebar.title("🎼 Navigation")
    st.sidebar.markdown("---")
    section = st.sidebar.radio("Choose Section:", 
                              ["🎭 Mood Analysis", "🎶 Music Parameters", "📊 Analytics", "ℹ️ About"])
    
    # Add user settings in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Settings")
    energy_level = st.sidebar.slider("Energy Level", 1, 10, 5)
    complexity = st.sidebar.select_slider("Complexity", ["Simple", "Moderate", "Complex"], "Moderate")

    if section == "🎭 Mood Analysis":
        st.markdown('<div class="mood-card">', unsafe_allow_html=True)
        st.header("🎭 Mood Analysis")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            user_input = st.text_area("Describe your mood, feelings, or the atmosphere you want:", 
                                    placeholder="e.g., I'm feeling energetic and ready to dance!")
            
            if st.button("🔍 Analyze Mood", type="primary"):
                if user_input:
                    try:
                        with st.spinner("Analyzing your mood..."):
                            mood = analyzer.analyze_mood(user_input)
                        
                        st.success("✅ Mood analysis complete!")
                        
                        # Display mood results in a nice format
                        if isinstance(mood, dict):
                            mood_category = mood.get("mood_category", "calm")
                            st.metric("Detected Mood", mood_category.title())
                            st.metric("Energy Level", f"{mood.get('energy_level', 5)}/10")
                            st.metric("Confidence", f"{mood.get('sentiment_confidence', 0.5):.2f}")
                            
                            # Create and display visualization
                            fig = create_mood_visualization(mood)
                            if fig and PLOTLY_AVAILABLE:
                                st.plotly_chart(fig, use_container_width=True)
                            elif not PLOTLY_AVAILABLE:
                                create_mood_visualization(mood)  # Uses fallback
                        else:
                            st.write(f"**Detected Mood:** {mood}")
                        
                    except Exception as e:
                        st.error(f"❌ An error occurred during mood analysis: {e}")
                else:
                    st.warning("Please enter a mood description first!")
        
        with col2:
            st.markdown("### 💡 Tips")
            st.info("""
            **For better results:**
            - Be descriptive about your feelings
            - Include context (time, activity, etc.)
            - Use emotional words
            - Mention energy levels
            """)

    elif section == "🎶 Music Parameters":
        st.markdown('<div class="parameter-card">', unsafe_allow_html=True)
        st.header("🎶 Music Parameters")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            mood_input = st.selectbox("Select a mood category:", 
                                    ["happy", "sad", "calm", "energetic", "mysterious", "romantic"])
            
            if st.button("🎵 Generate Parameters", type="primary"):
                try:
                    with st.spinner("Generating music parameters..."):
                        parameters = processor.enhance_parameters({
                            "mood_category": mood_input, 
                            "energy_level": energy_level
                        })
                    
                    st.success("✅ Parameters generated!")
                    
                    # Display parameters in an organized way
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.subheader("🎼 Musical Elements")
                        st.write(f"**Key:** {parameters.get('suggested_key', 'C')}")
                        st.write(f"**Tempo:** {parameters.get('tempo', 120)} BPM")
                        st.write(f"**Scale:** {parameters.get('scale_type', 'major')}")
                        st.write(f"**Dynamics:** {parameters.get('dynamics', 'mf')}")
                    
                    with col_right:
                        st.subheader("🎹 Arrangement")
                        st.write(f"**Texture:** {parameters.get('texture', 'homophonic')}")
                        st.write(f"**Pattern:** {parameters.get('rhythmic_pattern', 'straight')}")
                        if 'chord_progression' in parameters:
                            st.write(f"**Chords:** {' - '.join(parameters['chord_progression'])}")
                    
                    # Show full parameters
                    with st.expander("📋 View All Parameters"):
                        st.json(parameters)
                    
                    # Create and display visualization
                    fig = create_parameter_visualization(parameters)
                    if fig and PLOTLY_AVAILABLE:
                        st.plotly_chart(fig, use_container_width=True)
                    elif not PLOTLY_AVAILABLE:
                        create_parameter_visualization(parameters)  # Uses fallback
                    
                    # Generate and play audio
                    if MUSIC_GENERATOR_AVAILABLE and generator:
                        st.subheader("🎵 Generated Audio Preview")
                        audio_type = st.radio("Choose audio type:", ["Chord Progression", "Simple Melody"])
                        
                        if st.button("🎼 Generate Audio"):
                            try:
                                with st.spinner("Generating audio..."):
                                    if audio_type == "Chord Progression":
                                        audio = generator.generate_chord_progression(parameters)
                                    else:
                                        audio = generator.generate_melody(parameters)
                                    
                                    # Save audio file
                                    audio_filename = f"generated_music_{datetime.now().strftime('%H%M%S')}.wav"
                                    audio_path = generator.save_audio(audio, audio_filename)
                                    
                                    # Play audio
                                    st.audio(audio_filename)
                                    st.success("🎉 Audio generated successfully!")
                                    
                                    # Cleanup old files
                                    if os.path.exists(audio_filename):
                                        os.remove(audio_filename)
                                        
                            except Exception as e:
                                st.error(f"❌ Error generating audio: {e}")
                    else:
                        st.info("🎵 Audio generation requires additional dependencies. Check music_generator.py for requirements.")
                        
                except Exception as e:
                    st.error(f"❌ An error occurred during parameter generation: {e}")
        
        with col2:
            st.markdown("### 🎯 Parameters Guide")
            st.info("""
            **Key Elements:**
            - **Tempo:** Speed of the music
            - **Key:** Tonal center
            - **Scale:** Set of notes used
            - **Dynamics:** Volume levels
            - **Texture:** How parts interact
            """)

    elif section == "📊 Analytics":
        st.header("📊 Analytics Dashboard")
        
        if PLOTLY_AVAILABLE:
            # Sample analytics data
            st.subheader("🔥 Popular Moods")
            mood_data = pd.DataFrame({
                'Mood': ['Happy', 'Calm', 'Energetic', 'Sad', 'Mysterious'],
                'Count': [45, 38, 32, 28, 15]
            })
            
            fig = px.bar(mood_data, x='Mood', y='Count', 
                        title='Most Analyzed Moods This Week',
                        color='Count',
                        color_continuous_scale='plasma')
            st.plotly_chart(fig, use_container_width=True)
            
            # Tempo distribution
            st.subheader("🎵 Tempo Trends")
            tempo_data = pd.DataFrame({
                'Tempo Range': ['Slow (60-80)', 'Moderate (81-120)', 'Fast (121-160)', 'Very Fast (160+)'],
                'Percentage': [20, 45, 30, 5]
            })
            
            fig2 = px.pie(tempo_data, values='Percentage', names='Tempo Range',
                         title='Generated Tempo Distribution')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("📊 Analytics require Plotly. Install with: `pip install plotly`")
            
            # Fallback analytics
            st.subheader("🔥 Popular Moods")
            mood_data = pd.DataFrame({
                'Mood': ['Happy', 'Calm', 'Energetic', 'Sad', 'Mysterious'],
                'Count': [45, 38, 32, 28, 15]
            })
            st.bar_chart(mood_data.set_index('Mood'))
            
            st.subheader("🎵 Tempo Distribution")
            st.write("- Slow (60-80 BPM): 20%")
            st.write("- Moderate (81-120 BPM): 45%")
            st.write("- Fast (121-160 BPM): 30%")
            st.write("- Very Fast (160+ BPM): 5%")

    elif section == "ℹ️ About":
        st.header("ℹ️ About Symphony Muse")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### 🎵 Welcome to Symphony Muse
            
            Symphony Muse is an advanced AI-powered music composition tool that bridges the gap between 
            human emotions and musical expression. Using state-of-the-art natural language processing 
            and machine learning models, we analyze your mood and generate personalized music parameters 
            to inspire your creativity.
            
            ### ✨ Features
            - **Intelligent Mood Analysis**: Advanced sentiment analysis using Hugging Face models
            - **Music Theory Integration**: Scientifically-backed parameter generation
            - **Interactive Visualizations**: Real-time charts and graphs
            - **Customizable Settings**: Adjust energy levels and complexity
            - **Modern UI/UX**: Clean, responsive design
            
            ### 🚀 How It Works
            1. **Input**: Describe your mood or feelings
            2. **Analysis**: AI models process your input
            3. **Generation**: Music parameters are created
            4. **Visualization**: Results are displayed interactively
            
            ### 🛠️ Technology Stack
            - **Frontend**: Streamlit with custom CSS
            - **AI Models**: Hugging Face Transformers
            - **Visualizations**: Plotly
            - **Backend**: Python with pandas & numpy
            """)
        
        with col2:
            st.markdown("### 📈 Statistics")
            st.metric("Models Loaded", "2")
            st.metric("Mood Categories", "6")
            st.metric("Parameters Generated", "10+")
            
            st.markdown("### 🔗 Quick Links")
            st.markdown("""
            - [Documentation](https://example.com)
            - [GitHub Repository](https://github.com)
            - [Report Issues](https://github.com/issues)
            """)
            
            st.markdown("### 🎼 Music Theory")
            st.info("""
            Our parameters are based on established music theory principles including:
            - Circle of Fifths
            - Modal scales
            - Chord progressions
            - Rhythmic patterns
            """)

    # Footer
    st.markdown("---")
    st.markdown(f"<p style='text-align: center; color: #64748b;'>© 2025 Symphony Muse | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>", 
                unsafe_allow_html=True)

if __name__ == "__main__":
    main()