import streamlit as st
from datetime import datetime
from firebase_auth import firebase_auth
from user_auth import render_login_form, render_signup_form

def apply_custom_css():
    st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3rem;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
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
""", unsafe_allow_html=True)

def show_login_screen():
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="login-container">
            <h2>🎵 Welcome to AI Music Composer</h2>
            <p>Create personalized music using cutting-edge AI technology</p>
            <p><strong>Please log in or create an account to get started</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Create Account"])
    
    with tab1:
        st.subheader("Welcome Back!")
        render_login_form()
    
    with tab2:
        st.subheader("Join the AI Music Revolution!")
        render_signup_form()
    
    st.markdown("---")
    st.markdown("### 🌟 What You Can Do After Logging In:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🎭 Mood Analysis** - AI analyzes your text")
    with col2:
        st.markdown("**🎵 Music Generation** - 30-second compositions")
    with col3:
        st.markdown("**💾 Personal Library** - Save your creations")

def show_main_app():
    st.sidebar.title("🎼 Navigation")
    user = firebase_auth.get_current_user()
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"👤 **{user.get('display_name', 'User')}**")
    st.sidebar.markdown(f"📧 {user.get('email', '')}")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        firebase_auth.logout_user()
        st.rerun()
    
    st.success("🎉 You are logged in! All music generation features are now available.")
    st.info("✅ Authentication is working correctly - you can only see this after logging in!")

def main():
    st.set_page_config(
        page_title="AI Music Composer", 
        page_icon="🎵", 
        layout="wide"
    )
    
    apply_custom_css()
    st.markdown('<h1 class="main-header">🎵 AI Music Composer</h1>', unsafe_allow_html=True)
    
    # MANDATORY AUTHENTICATION CHECK
    if not firebase_auth.is_user_logged_in():
        show_login_screen()
        return
    
    show_main_app()

if __name__ == "__main__":
    main()
