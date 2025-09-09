import streamlit as st
from firebase_auth import firebase_auth
import hashlib
import os

def render_login_form():
    """Render login form"""
    st.markdown("### 🔐 Login to Your Account")
    
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="your.email@example.com")
        password = st.text_input("🔒 Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("🚀 Login", use_container_width=True)
        with col2:
            signup_button = st.form_submit_button("📝 Sign Up", use_container_width=True)
        
        if login_button:
            if email and password:
                user = firebase_auth.authenticate_user(email, password)
                if user:
                    st.success(f"✅ Welcome back, {user.get('display_name', 'User')}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password")
            else:
                st.warning("⚠️ Please enter both email and password")
        
        if signup_button:
            st.session_state['show_signup'] = True
            st.rerun()

def render_signup_form():
    """Render signup form"""
    st.markdown("### 📝 Create New Account")
    
    with st.form("signup_form"):
        display_name = st.text_input("👤 Display Name", placeholder="Your Name")
        email = st.text_input("📧 Email", placeholder="your.email@example.com")
        password = st.text_input("🔒 Password", type="password")
        confirm_password = st.text_input("🔒 Confirm Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            create_button = st.form_submit_button("✨ Create Account", use_container_width=True)
        with col2:
            back_button = st.form_submit_button("⬅️ Back to Login", use_container_width=True)
        
        if create_button:
            if not all([display_name, email, password, confirm_password]):
                st.error("❌ Please fill in all fields")
            elif password != confirm_password:
                st.error("❌ Passwords don't match")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters")
            else:
                user = firebase_auth.create_user_account(email, password, display_name)
                if user:
                    st.success("✅ Account created successfully! Please login.")
                    st.session_state['show_signup'] = False
                    st.rerun()
        
        if back_button:
            st.session_state['show_signup'] = False
            st.rerun()

def render_user_profile():
    """Render user profile and preferences"""
    user = firebase_auth.get_current_user()
    if not user:
        return
    
    st.markdown("### 👤 User Profile")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Name:** {user.get('display_name', 'Unknown')}")
        st.markdown(f"**Email:** {user.get('email', 'Unknown')}")
        st.markdown(f"**Member since:** {user.get('created_at', 'Unknown')[:10]}")
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            firebase_auth.logout_user()
            st.rerun()
    
    # User Preferences
    st.markdown("### ⚙️ Music Preferences")
    
    preferences = firebase_auth.get_user_preferences(user.get('uid'))
    
    with st.form("preferences_form"):
        favorite_mood = st.selectbox(
            "🎭 Favorite Mood:",
            ["happy", "sad", "calm", "energetic", "mysterious", "romantic"],
            index=["happy", "sad", "calm", "energetic", "mysterious", "romantic"].index(
                preferences.get('favorite_mood', 'happy')
            )
        )
        
        preferred_tempo = st.slider(
            "🎵 Preferred Tempo (BPM):",
            60, 180,
            preferences.get('preferred_tempo', 120)
        )
        
        preferred_instruments = st.multiselect(
            "🎸 Preferred Instruments:",
            ["piano", "guitar", "drums", "strings", "synth", "brass", "flute", "bass"],
            default=preferences.get('preferred_instruments', ['piano', 'guitar'])
        )
        
        if st.form_submit_button("💾 Save Preferences"):
            new_preferences = {
                'favorite_mood': favorite_mood,
                'preferred_tempo': preferred_tempo,
                'preferred_instruments': preferred_instruments
            }
            
            if firebase_auth.update_user_preferences(user.get('uid'), new_preferences):
                st.success("✅ Preferences saved!")
                st.rerun()

def render_user_music_history():
    """Render user's music generation history"""
    user = firebase_auth.get_current_user()
    if not user:
        return
    
    st.markdown("### 🎵 Your Music History")
    
    history = firebase_auth.get_user_music_history(user.get('uid'))
    
    if not history:
        st.info("🎼 No music generated yet. Start creating some music!")
        return
    
    # Display history in reverse chronological order
    for i, entry in enumerate(reversed(history[-10:])):  # Show last 10 entries
        with st.expander(f"🎵 {entry.get('mood_category', 'Unknown').title()} Music - {entry.get('timestamp', '')[:16]}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Original Input:** {entry.get('mood_input', 'N/A')}")
                st.markdown(f"**Mood:** {entry.get('mood_category', 'N/A').title()}")
                st.markdown(f"**Energy Level:** {entry.get('energy_level', 'N/A')}/10")
            
            with col2:
                st.markdown(f"**Tempo:** {entry.get('tempo', 'N/A')} BPM")
                st.markdown(f"**Key:** {entry.get('key', 'N/A').title()}")
                st.markdown(f"**Instruments:** {', '.join(entry.get('instruments', []))}")
            
            # If audio file exists, show player
            audio_path = entry.get('audio_file_path')
            if audio_path and os.path.exists(audio_path):
                try:
                    with open(audio_path, 'rb') as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format='audio/mp3')
                except:
                    st.info("🎵 Audio file no longer available")

def render_music_stats():
    """Render user's music generation statistics"""
    user = firebase_auth.get_current_user()
    if not user:
        return
    
    history = firebase_auth.get_user_music_history(user.get('uid'))
    
    if not history:
        return
    
    st.markdown("### 📊 Your Music Stats")
    
    # Calculate statistics
    total_generated = len(history)
    mood_counts = {}
    avg_energy = 0
    avg_tempo = 0
    
    for entry in history:
        mood = entry.get('mood_category', 'unknown')
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
        avg_energy += entry.get('energy_level', 5)
        avg_tempo += entry.get('tempo', 120)
    
    if total_generated > 0:
        avg_energy = avg_energy / total_generated
        avg_tempo = avg_tempo / total_generated
    
    # Display stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎵 Total Generated", total_generated)
    
    with col2:
        st.metric("⚡ Avg Energy", f"{avg_energy:.1f}/10")
    
    with col3:
        st.metric("🎼 Avg Tempo", f"{avg_tempo:.0f} BPM")
    
    with col4:
        most_common_mood = max(mood_counts, key=mood_counts.get) if mood_counts else "None"
        st.metric("🎭 Favorite Mood", most_common_mood.title())
    
    # Mood distribution chart
    if mood_counts:
        import pandas as pd
        mood_df = pd.DataFrame(list(mood_counts.items()), columns=['Mood', 'Count'])
        st.bar_chart(mood_df.set_index('Mood'))

def check_authentication():
    """Check if user is authenticated and show login if not"""
    if not firebase_auth.is_user_logged_in():
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("## 🔐 User Authentication")
        st.markdown("*Login to save your music creations and preferences*")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show signup form if requested
        if st.session_state.get('show_signup', False):
            render_signup_form()
        else:
            render_login_form()
            
            # Demo account info
            st.markdown("---")
            st.info("""
            💡 **Demo Mode Available**
            
            You can use any email/password combination to try the demo.
            Your data will be stored locally during this session.
            
            For production use, configure Firebase in `firebase_auth.py`
            """)
        
        return False
    
    return True

def save_music_to_user_profile(music_data, generation_method="mood_analysis"):
    """Save generated music to user's profile"""
    user = firebase_auth.get_current_user()
    if user:
        music_data['generation_method'] = generation_method
        success = firebase_auth.save_user_music_generation(user.get('uid'), music_data)
        if success:
            st.success("💾 Music saved to your profile!")
        return success
    return False


def render_music_stats():
    """Render user music statistics."""
    st.header("📊 Your Music Statistics")
    
    # Get user's music history from Firebase
    user_data = firebase_auth.get_user_data()
    if not user_data or 'music_history' not in user_data:
        st.info("📈 Start generating music to see your statistics!")
        return
    
    music_history = user_data['music_history']
    
    # Basic stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎵 Total Tracks", len(music_history))
    
    with col2:
        moods = [m.get('mood_category', 'Unknown') for m in music_history]
        most_common_mood = max(set(moods), key=moods.count) if moods else "None"
        st.metric("🎭 Favorite Mood", most_common_mood)
    
    with col3:
        creation_dates = [m.get('created_at', '') for m in music_history if m.get('created_at')]
        if creation_dates:
            from datetime import datetime
            recent_tracks = len([d for d in creation_dates if d.startswith(datetime.now().strftime('%Y-%m'))])
            st.metric("📅 This Month", recent_tracks)
        else:
            st.metric("📅 This Month", 0)
    
    # Mood distribution
    st.subheader("🎭 Mood Distribution")
    if moods:
        import pandas as pd
        mood_counts = pd.Series(moods).value_counts()
        st.bar_chart(mood_counts)
    else:
        st.info("Generate some music to see mood distribution!")
    
    # Recent activity
    st.subheader("📅 Recent Activity")
    if music_history:
        recent_tracks = sorted(music_history, 
                             key=lambda x: x.get('created_at', ''), 
                             reverse=True)[:5]
        
        for track in recent_tracks:
            with st.expander(f"🎵 {track.get('title', 'Untitled')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Prompt:** {track.get('user_prompt', 'N/A')}")
                    st.write(f"**Mood:** {track.get('mood_category', 'Unknown')}")
                with col2:
                    st.write(f"**Created:** {track.get('created_at', 'Unknown')}")
                    if track.get('audio_file'):
                        st.write(f"**File:** {track['audio_file']}")
    else:
        st.info("No music generated yet!")


def check_authentication():
    """Check if user is authenticated and show login forms if not."""
    if not firebase_auth.is_user_logged_in():
        # Show authentication forms
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab1:
            render_login_form()
        
        with tab2:
            render_signup_form()
        
        return False
    return True
