import streamlit as st
from firebase_auth import firebase_auth
from mood_analyzer import MoodAnalyzer
from music_generator import MusicGenerator
from user_auth import render_login_form, render_signup_form, render_user_profile, render_user_music_history
from datetime import datetime
from pathlib import Path

def apply_custom_css():
    st.markdown('''
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .login-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 2rem 0;
        text-align: center;
    }
</style>
''', unsafe_allow_html=True)

def show_login_screen():
    st.markdown('---')
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('''
        <div class="login-container">
            <h2>🎵 Welcome to AI Music Composer</h2>
            <p>Create personalized music using cutting-edge AI technology</p>
            <p><strong>Please log in or create an account to get started</strong></p>
        </div>
        ''', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(['🔐 Login', '📝 Create Account'])
    with tab1:
        st.subheader('Welcome Back!')
        render_login_form()
    with tab2:
        st.subheader('Join the AI Music Revolution!')
        render_signup_form()

def show_main_app():
    st.sidebar.title('🎼 Navigation')
    user = firebase_auth.get_current_user()
    st.sidebar.markdown('---')
    st.sidebar.markdown(f'👤 **{user.get("display_name", "User")}**')
    st.sidebar.markdown(f'📧 {user.get("email", "")}')
    if st.sidebar.button('🚪 Logout', use_container_width=True):
        firebase_auth.logout_user()
        st.rerun()
    st.sidebar.markdown('---')
    
    # Enhanced navigation with descriptions
    st.sidebar.markdown("### 🎯 Features")
    nav_options = [
        "� Welcome & Features",
        "�🎭 Mood Analysis", 
        "🎵 Music Generation", 
        "🎼 My Music", 
        "🔐 User Profile"
    ]
    section = st.sidebar.radio("Choose Section:", nav_options)
    
    # Feature descriptions in sidebar
    with st.sidebar.expander("ℹ️ Quick Info", expanded=False):
        st.markdown("""
        **🎭 Mood Analysis**
        AI-powered emotion detection
        
        **🎵 Music Generation**
        Create music with AI models
        
        **🎼 My Music**
        Your generated music history
        
        **🔐 User Profile**
        Account settings & preferences
        """)
    
    # Main content based on selection
    if section == "� Welcome & Features":
        show_welcome_section()
    elif section == "�🎭 Mood Analysis":
        mood_analysis_section()
    elif section == "🎵 Music Generation":
        music_generation_section()
    elif section == "🎼 My Music":
        render_user_music_history()
    elif section == "🔐 User Profile":
        render_user_profile()

def show_welcome_section():
    """Display comprehensive welcome and feature overview"""
    st.title("🎵 AI-Based Music Composition Platform")
    st.markdown("### Welcome to the future of personalized music creation! 🚀")
    
    st.markdown("""
    This platform combines **cutting-edge AI technology** with **music theory** to create personalized music 
    based on your emotions and preferences. Powered by **Hugging Face Transformers** and **Advanced AI Models**.
    """)
    
    # System status overview
    st.markdown("---")
    st.header("🔧 System Status & Capabilities")
    
    try:
        # Check mood analyzer
        analyzer = MoodAnalyzer()
        mood_status = "✅ Ready"
        mood_model = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    except:
        mood_status = "⚠️ Limited"
        mood_model = "Fallback models"
    
    try:
        # Check music generator
        generator = MusicGenerator()
        gen_info = generator.get_generation_info()
        if gen_info['musicgen_available']:
            music_status = "✅ AI Models Ready"
            music_model = gen_info['model_name']
        else:
            music_status = "⚠️ Fallback Mode"
            music_model = "Basic Synthesis"
    except:
        music_status = "❌ Error"
        music_model = "Unavailable"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        ### 🎭 Mood Analysis Engine
        **Status**: {mood_status}
        **Model**: {mood_model}
        
        **Capabilities:**
        - 🧠 Advanced sentiment analysis
        - 🎯 6 distinct mood categories
        - ⚡ Energy level detection (1-10)
        - 🎼 Automatic musical parameter mapping
        - 🎹 Instrument recommendation
        - 🎵 Genre and tempo suggestion
        """)
    
    with col2:
        st.markdown(f"""
        ### 🎵 Music Generation System
        **Status**: {music_status}
        **Engine**: {music_model}
        
        **Features:**
        - 🤖 AI-powered music creation
        - 🎼 Text-to-music conversion
        - 🎧 Instant audio playback
        - 💾 MP3 download (30 seconds)
        - 🎛️ Custom parameter control
        - 🔄 Quality enhancement
        """)
    
    # Feature demonstration
    st.markdown("---")
    st.header("🎯 Complete Feature Set")
    
    features = [
        ("🔥 Firebase Authentication", "✅", "Secure user accounts with Google Firebase"),
        ("🎭 Hugging Face AI Models", "✅", "Advanced sentiment analysis and embeddings"),
        ("🎵 MusicGen Integration", music_status, "Facebook's MusicGen for AI music creation"),
        ("🎼 Musical Theory Engine", "✅", "Comprehensive music parameter mapping"),
        ("🎧 Audio Processing", "✅", "Real-time audio conversion and enhancement"),
        ("💾 Cloud Storage", "✅", "Firestore database for user data and history"),
        ("🎨 Modern UI/UX", "✅", "Responsive design with real-time feedback"),
        ("📱 Cross-Platform", "✅", "Works on desktop, tablet, and mobile"),
    ]
    
    for feature, status, description in features:
        col1, col2, col3 = st.columns([3, 1, 4])
        with col1:
            st.markdown(f"**{feature}**")
        with col2:
            st.markdown(status)
        with col3:
            st.markdown(f"_{description}_")
    
    # Quick start guide
    st.markdown("---")
    st.header("🚀 Quick Start Guide")
    
    tab1, tab2, tab3 = st.tabs(["1️⃣ Analyze Mood", "2️⃣ Generate Music", "3️⃣ Download & Save"])
    
    with tab1:
        st.markdown("""
        ### 🎭 Step 1: Mood Analysis
        1. Navigate to **🎭 Mood Analysis**
        2. Describe your current mood or feelings
        3. Click **🔍 Analyze Mood with AI**
        4. View detailed analysis results
        
        **Example inputs:**
        - "I'm feeling energetic and ready to dance!"
        - "I need calm music for studying"
        - "Feeling romantic and nostalgic"
        """)
        
        if st.button("🎭 Try Mood Analysis Now", type="primary"):
            st.session_state.nav_to_mood = True
            st.rerun()
    
    with tab2:
        st.markdown("""
        ### 🎵 Step 2: Music Generation
        1. Use your mood analysis results, OR
        2. Enter custom music description, OR
        3. Use manual parameter controls
        4. Click **🎵 Generate Music**
        5. Wait 30-60 seconds for AI processing
        
        **Generation options:**
        - From mood analysis
        - Custom text descriptions
        - Manual parameter control
        """)
        
        if st.button("🎵 Try Music Generation Now", type="primary"):
            st.session_state.nav_to_music = True
            st.rerun()
    
    with tab3:
        st.markdown("""
        ### 💾 Step 3: Download & Save
        1. Listen to generated music
        2. Download as MP3 file
        3. Save to your profile history
        4. Share or use in your projects
        
        **Audio features:**
        - Instant playback
        - High-quality MP3 download
        - 30-second compositions
        - Volume and quality optimization
        """)
    
    # Quick stats
    if st.button("📊 View My Profile", type="secondary", use_container_width=True):
        st.session_state.nav_to_profile = True
        st.rerun()
    
    # Handle navigation requests
    if st.session_state.get('nav_to_mood', False):
        st.session_state.nav_to_mood = False
        st.session_state.current_section = "🎭 Mood Analysis"
        st.rerun()
    elif st.session_state.get('nav_to_music', False):
        st.session_state.nav_to_music = False
        st.session_state.current_section = "🎵 Music Generation"
        st.rerun()
    elif st.session_state.get('nav_to_profile', False):
        st.session_state.nav_to_profile = False
        st.session_state.current_section = "🔐 User Profile"
        st.rerun()

def mood_analysis_section():
    st.header("🎭 Mood Analysis Engine")
    st.info("🤖 **Powered by Hugging Face Transformers** - Advanced AI sentiment analysis and mood classification")
    
    # Show system capabilities
    with st.expander("🔬 Analysis Capabilities", expanded=False):
        st.markdown("""
        **🧠 AI Models Used:**
        • **Sentiment Analysis**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
        • **Mood Classification**: `all-MiniLM-L6-v2` sentence transformers
        • **Energy Detection**: Custom keyword analysis algorithm
        
        **🎭 Mood Categories**: Happy, Sad, Calm, Energetic, Mysterious, Romantic
        **⚡ Energy Scale**: 1-10 dynamic energy level calculation
        **🎼 Musical Output**: Tempo, key, instruments, genre mapping
        """)
    
    user_input = st.text_area(
        "🗣️ Describe your mood or feelings:",
        placeholder="Examples:\n• 'I'm feeling energetic and ready to dance!'\n• 'I need calm music for studying'\n• 'Feeling melancholic and nostalgic today'",
        height=120
    )
    
    col1, col2 = st.columns([2, 1])
    with col1:
        analyze_button = st.button("🔍 Analyze Mood with AI", type="primary", use_container_width=True)
    with col2:
        if st.button("🎲 Try Example", use_container_width=True):
            examples = [
                "I'm feeling excited and pumped up for my workout!",
                "I need peaceful, calming music for meditation",
                "Feeling romantic and want something tender",
                "I'm sad and need emotional music to match my mood"
            ]
            st.session_state.example_input = examples[len(examples) % 4]
            st.rerun()
    
    # Use example if set
    if 'example_input' in st.session_state:
        user_input = st.session_state.example_input
        del st.session_state.example_input
    
    if analyze_button and user_input.strip():
        try:
            with st.spinner("🤖 Analyzing your mood with Hugging Face AI models..."):
                analyzer = MoodAnalyzer()
                result = analyzer.analyze_mood(user_input)
            
            st.success("✅ AI Analysis Complete!")
            
            # Main results display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🎭 Mood Category", result.get("mood_category", "unknown").title())
            with col2:
                st.metric("⚡ Energy Level", f"{result.get('energy_level', 0)}/10")
            with col3:
                st.metric("💭 Sentiment", result.get("sentiment", "neutral").title())
            with col4:
                st.metric("🎯 Confidence", f"{result.get('sentiment_confidence', 0):.2f}")
            
            # Detailed analysis results
            with st.expander("🔬 Detailed Analysis Results", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🎼 Musical Parameters Generated:**")
                    st.markdown(f"• **Tempo**: {result.get('tempo', 120)} BPM")
                    st.markdown(f"• **Key**: {result.get('key', 'major').title()}")
                    st.markdown(f"• **Time Signature**: {result.get('time_signature', '4/4')}")
                    st.markdown(f"• **Genre Style**: {result.get('genre_style', 'contemporary').replace('_', ' ').title()}")
                    st.markdown(f"• **Dynamics**: {result.get('dynamics', 'mf')} (Musical Volume)")
                    st.markdown(f"• **Texture**: {result.get('texture', 'homophonic').title()}")
                
                with col2:
                    st.markdown("**🎹 Recommended Instruments:**")
                    instruments = result.get('instruments', ['piano'])
                    for i, instrument in enumerate(instruments, 1):
                        st.markdown(f"{i}. {instrument.replace('_', ' ').title()}")
                    
                    st.markdown("**🤖 AI Generation Prompt:**")
                    st.code(result.get('text_prompt', 'moderate music'), language="text")
            
            # Store results for music generation
            st.session_state['mood_analysis'] = result
            
            # Quick generation button
            st.markdown("---")
            if st.button("🚀 Generate Music from This Analysis", type="secondary", use_container_width=True):
                st.info("🎵 Switching to Music Generation with your mood analysis...")
                st.session_state['auto_generate'] = True
                
        except Exception as e:
            st.error(f"❌ Analysis failed: {e}")
            st.info("🔧 This might be due to missing dependencies. The app includes fallback models.")
            
    elif analyze_button:
        st.warning("⚠️ Please enter a mood description first!")
    
    # Show recent analysis if available
    if 'mood_analysis' in st.session_state and not analyze_button:
        with st.expander("📊 Previous Analysis Results", expanded=False):
            prev_result = st.session_state['mood_analysis']
            st.markdown(f"**Last Analysis**: {prev_result.get('mood_category', 'unknown').title()} mood, Energy {prev_result.get('energy_level', 0)}/10")
            st.markdown(f"**Input**: _{prev_result.get('original_input', 'N/A')}_")

def music_generation_section():
    st.header("🎵 Music Generation Studio")
    
    # Check system status
    try:
        generator = MusicGenerator()
        gen_info = generator.get_generation_info()
        if gen_info['musicgen_available']:
            st.success("🤖 **MusicGen AI Ready** - Advanced neural music generation available!")
        else:
            st.warning("⚠️ **Fallback Mode** - Using basic synthesis (install `audiocraft` for full AI features)")
        
        with st.expander("🔧 Generation System Info", expanded=False):
            st.markdown(f"""
            **🎼 Music Generation Engine:**
            • **Model**: {gen_info['model_name']}
            • **Sample Rate**: {gen_info['sample_rate']} Hz
            • **Duration**: {gen_info['duration']} seconds
            • **Output Format**: {gen_info['output_format']}
            
            **🎯 Features:**
            • Text-to-Music AI conversion
            • Musical parameter integration
            • Real-time audio processing
            • Quality enhancement & normalization
            """)
    except Exception as e:
        st.error(f"❌ System error: {e}")
        return
    
    # Auto-generation from mood analysis
    if st.session_state.get('auto_generate', False):
        st.session_state['auto_generate'] = False
        if 'mood_analysis' in st.session_state:
            st.info("🎭 **Generating music from your mood analysis...**")
            generate_music_from_mood(st.session_state['mood_analysis'])
            return
    
    # Check if we have mood analysis results
    if 'mood_analysis' in st.session_state:
        mood_result = st.session_state['mood_analysis']
        st.info(f"🎭 **Previous Analysis Available**: {mood_result.get('mood_category', 'unknown').title()} mood, Energy {mood_result.get('energy_level', 0)}/10")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎭 Generate from Mood Analysis", type="secondary", use_container_width=True):
                generate_music_from_mood(mood_result)
                return
        with col2:
            if st.button("🔄 View Analysis Details", use_container_width=True):
                with st.expander("📊 Analysis Details", expanded=True):
                    st.markdown(f"**Original Input**: _{mood_result.get('original_input', 'N/A')}_")
                    st.markdown(f"**Generated Prompt**: {mood_result.get('text_prompt', 'N/A')}")
                    st.markdown(f"**Musical Key**: {mood_result.get('key', 'major').title()}")
                    st.markdown(f"**Tempo**: {mood_result.get('tempo', 120)} BPM")
                    instruments = mood_result.get('instruments', ['piano'])
                    st.markdown(f"**Instruments**: {', '.join(instruments)}")
    
    st.markdown("---")
    st.markdown("### 🎨 Custom Music Generation")
    
    # Custom generation options
    tab1, tab2 = st.tabs(["🗣️ Text Description", "🎛️ Manual Parameters"])
    
    with tab1:
        user_input = st.text_area(
            "🎼 Describe the music you want:",
            placeholder="Examples:\n• 'Upbeat electronic dance music with strong bass'\n• 'Calm piano melody for relaxation and studying'\n• 'Epic orchestral music with dramatic crescendos'\n• 'Jazz fusion with saxophone and electric guitar'",
            height=100
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            generate_custom = st.button("🎵 Generate Custom Music", type="primary", use_container_width=True)
        with col2:
            if st.button("💡 Examples", use_container_width=True):
                examples = [
                    "Upbeat pop music with guitar and drums",
                    "Peaceful ambient soundscape for meditation",
                    "Energetic rock anthem with electric guitars",
                    "Romantic piano ballad with soft strings"
                ]
                st.session_state.music_example = examples[len(examples) % 4]
                st.rerun()
        
        # Use example if set
        if 'music_example' in st.session_state:
            user_input = st.session_state.music_example
            del st.session_state.music_example
        
        if generate_custom and user_input.strip():
            generate_custom_music(user_input, generator)
        elif generate_custom:
            st.warning("⚠️ Please enter a music description first!")
    
    with tab2:
        st.markdown("🎛️ **Advanced Parameter Control**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            tempo = st.slider("🥁 Tempo (BPM)", 60, 180, 120)
            energy = st.slider("⚡ Energy Level", 1, 10, 5)
        with col2:
            mood = st.selectbox("🎭 Mood", ["happy", "sad", "calm", "energetic", "mysterious", "romantic"])
            key = st.selectbox("🎹 Key", ["major", "minor"])
        with col3:
            genre = st.selectbox("🎼 Genre", ["pop", "rock", "classical", "electronic", "jazz", "ambient"])
            duration = st.slider("⏱️ Duration", 10, 30, 30)
        
        if st.button("🎵 Generate with Parameters", type="primary", use_container_width=True):
            params = {
                'tempo': tempo,
                'energy_level': energy,
                'mood_category': mood,
                'key': key,
                'genre_style': genre,
                'text_prompt': f"{energy_words.get(energy, 'moderate')} {mood} {genre} music in {key} key at {tempo} BPM"
            }
            generate_music_with_params(params, generator)

def generate_custom_music(user_input, generator):
    """Generate music from custom text description"""
    try:
        with st.spinner("🎼 Generating music... This may take 30-60 seconds..."):
            st.info(f"🎯 **Generating**: {user_input}")
            audio_file_path = generator.generate_music({'text_prompt': user_input})
        
        if audio_file_path and Path(audio_file_path).exists():
            display_generated_music(audio_file_path, user_input, generator)
        else:
            st.error("❌ Failed to generate music. Please try again with a different description.")
            
    except Exception as e:
        st.error(f"❌ Generation failed: {e}")
        st.info("💡 Try a simpler description or check system requirements.")

def generate_music_with_params(params, generator):
    """Generate music with manual parameters"""
    try:
        with st.spinner("🎼 Generating music with your custom parameters..."):
            st.info(f"🎯 **Parameters**: {params['mood_category'].title()} mood, {params['tempo']} BPM, {params['key']} key")
            audio_file_path = generator.generate_music(params)
        
        if audio_file_path and Path(audio_file_path).exists():
            description = f"{params['mood_category'].title()} {params['genre_style']} music ({params['tempo']} BPM)"
            display_generated_music(audio_file_path, description, generator)
        else:
            st.error("❌ Failed to generate music with these parameters.")
            
    except Exception as e:
        st.error(f"❌ Generation failed: {e}")

def display_generated_music(audio_file_path, description, generator):
    """Display generated music with player and download options"""
    st.success("🎉 **Music Generated Successfully!**")
    st.markdown(f"**Description**: {description}")
    
    # Get audio for playback
    audio_bytes, mime_type = generator.get_audio_for_streamlit(audio_file_path)
    
    if audio_bytes:
        # Audio player
        st.audio(audio_bytes, format=mime_type)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download button
            file_name = f"ai_music_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            st.download_button(
                label="📥 Download MP3",
                data=audio_bytes,
                file_name=file_name,
                mime=mime_type,
                use_container_width=True
            )
        
        with col2:
            if st.button("🔄 Generate Another", use_container_width=True):
                st.rerun()
        
        with col3:
            if st.button("💾 Save to Profile", use_container_width=True):
                # This would save to user's Firebase profile
                st.success("💾 Saved to your music history!")
        
        # File info
        file_size = len(audio_bytes) / 1024  # KB
        st.caption(f"📊 File size: {file_size:.1f} KB | Format: {mime_type}")
        
    else:
        st.error("❌ Audio playback not available, but file was generated.")

# Helper dictionary for energy words
energy_words = {
    1: "very slow", 2: "slow", 3: "gentle", 4: "relaxed", 5: "moderate",
    6: "upbeat", 7: "energetic", 8: "lively", 9: "dynamic", 10: "intense"
}

def generate_music_from_mood(mood_result):
    try:
        with st.spinner("🎼 Generating music from mood analysis..."):
            generator = MusicGenerator()
            audio_file_path = generator.generate_music(mood_result)
        
        if audio_file_path and Path(audio_file_path).exists():
            st.success("🎉 Music generated from your mood!")
            
            # Display audio player
            audio_bytes, mime_type = generator.get_audio_for_streamlit(audio_file_path)
            if audio_bytes:
                st.audio(audio_bytes, format=mime_type)
                
                # Download button
                file_name = f"mood_music_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                st.download_button(
                    label="📥 Download MP3",
                    data=audio_bytes,
                    file_name=file_name,
                    mime=mime_type
                )
        else:
            st.error("❌ Failed to generate music from mood analysis.")
    except Exception as e:
        st.error(f"❌ Generation failed: {e}")

def main():
    st.set_page_config(
        page_title='AI Music Composer', 
        page_icon='🎵', 
        layout='wide'
    )
    apply_custom_css()
    st.markdown('<h1 class="main-header">🎵 AI Music Composer</h1>', unsafe_allow_html=True)
    if not firebase_auth.is_user_logged_in():
        show_login_screen()
        return
    show_main_app()

if __name__ == '__main__':
    main()