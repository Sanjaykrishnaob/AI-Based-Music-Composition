# Firebase Configuration
import firebase_admin
from firebase_admin import credentials, firestore, auth
import streamlit as st
import json
from datetime import datetime
import os

class FirebaseAuth:
    """Firebase Authentication and Database Handler"""
    
    def __init__(self):
        self.db = None
        self.initialize_firebase()
    
    def initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Try to load service account key
                service_account_path = 'firebase-service-account.json'
                
                if os.path.exists(service_account_path):
                    try:
                        # Load and validate service account
                        with open(service_account_path, 'r') as f:
                            service_account_data = json.load(f)
                        
                        # Check if it's a valid service account
                        required_fields = ['type', 'project_id', 'private_key', 'client_email']
                        if all(field in service_account_data for field in required_fields):
                            if service_account_data.get('type') == 'service_account':
                                # Initialize with real Firebase
                                cred = credentials.Certificate(service_account_path)
                                firebase_admin.initialize_app(cred)
                                
                                # Try to initialize Firestore, but continue if it fails
                                try:
                                    self.db = firestore.client()
                                    print("🔥 Firebase Admin SDK with Firestore initialized successfully!")
                                except Exception as firestore_error:
                                    print(f"🔥 Firebase Admin SDK initialized (Firestore not available: {firestore_error})")
                                    self.db = None
                                
                                st.session_state['firebase_demo'] = False
                                return
                    except Exception as e:
                        print(f"Service account error: {e}")
                
                # Fallback to demo mode
                st.session_state['firebase_demo'] = True
                print("🔧 Firebase demo mode initialized")
            else:
                # Firebase already initialized
                if not st.session_state.get('firebase_demo'):
                    try:
                        self.db = firestore.client()
                    except Exception as firestore_error:
                        print(f"Firestore connection failed: {firestore_error}")
                        self.db = None
            
        except Exception as e:
            print(f"Firebase initialization error: {e}")
            st.session_state['firebase_demo'] = True
    
    def create_user_account(self, email, password, display_name):
        """Create a new user account"""
        try:
            if st.session_state.get('firebase_demo'):
                # Demo mode - simulate user creation
                user_data = {
                    'uid': f"demo_user_{hash(email) % 10000}",
                    'email': email,
                    'display_name': display_name,
                    'created_at': datetime.now().isoformat(),
                    'music_history': [],
                    'preferences': {
                        'favorite_mood': 'happy',
                        'preferred_tempo': 120,
                        'preferred_instruments': ['piano', 'guitar']
                    }
                }
                st.session_state['demo_user'] = user_data
                return user_data
            else:
                # Real Firebase user creation - but handle Firestore errors
                try:
                    # Create user with Firebase Auth only
                    user = auth.create_user(
                        email=email,
                        password=password,
                        display_name=display_name
                    )
                    
                    # Try to create user document in Firestore, but fall back gracefully
                    try:
                        if self.db:
                            user_doc = {
                                'email': email,
                                'display_name': display_name,
                                'created_at': datetime.now(),
                                'music_history': [],
                                'preferences': {
                                    'favorite_mood': 'happy',
                                    'preferred_tempo': 120,
                                    'preferred_instruments': ['piano', 'guitar']
                                }
                            }
                            self.db.collection('users').document(user.uid).set(user_doc)
                    except Exception as firestore_error:
                        # Firestore not available, but Auth user created successfully
                        print(f"Firestore error (user still created): {firestore_error}")
                    
                    # Return user data in session format
                    user_data = {
                        'uid': user.uid,
                        'email': email,
                        'display_name': display_name,
                        'created_at': datetime.now().isoformat(),
                        'music_history': [],
                        'preferences': {
                            'favorite_mood': 'happy',
                            'preferred_tempo': 120,
                            'preferred_instruments': ['piano', 'guitar']
                        }
                    }
                    st.session_state['current_user'] = user_data
                    return user_data
                    
                except Exception as auth_error:
                    # If Firebase Auth also fails, fall back to demo mode
                    print(f"Firebase Auth error, falling back to demo: {auth_error}")
                    st.session_state['firebase_demo'] = True
                    return self.create_user_account(email, password, display_name)
                
        except Exception as e:
            st.error(f"Error creating account: {e}")
            return None
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        try:
            if st.session_state.get('firebase_demo'):
                # Demo mode - simple validation
                if email and password:
                    user_data = {
                        'uid': f"demo_user_{hash(email) % 10000}",
                        'email': email,
                        'display_name': email.split('@')[0],
                        'created_at': datetime.now().isoformat(),
                        'music_history': st.session_state.get('demo_music_history', []),
                        'preferences': st.session_state.get('demo_preferences', {
                            'favorite_mood': 'happy',
                            'preferred_tempo': 120,
                            'preferred_instruments': ['piano', 'guitar']
                        })
                    }
                    st.session_state['current_user'] = user_data
                    return user_data
                return None
            else:
                # Real Firebase authentication would go here
                # This requires Firebase client SDK integration
                pass
                
        except Exception as e:
            st.error(f"Authentication error: {e}")
            return None
    
    def save_user_music_generation(self, user_id, music_data):
        """Save generated music to user's history"""
        try:
            music_entry = {
                'timestamp': datetime.now().isoformat(),
                'mood_input': music_data.get('original_input', ''),
                'mood_category': music_data.get('mood_category', ''),
                'energy_level': music_data.get('energy_level', 5),
                'tempo': music_data.get('tempo', 120),
                'key': music_data.get('key', 'major'),
                'instruments': music_data.get('instruments', []),
                'audio_file_path': music_data.get('audio_file_path', ''),
                'generation_method': music_data.get('generation_method', 'mood_analysis')
            }
            
            if st.session_state.get('firebase_demo'):
                # Demo mode - store in session
                if 'demo_music_history' not in st.session_state:
                    st.session_state['demo_music_history'] = []
                st.session_state['demo_music_history'].append(music_entry)
                
                # Update current user data
                if 'current_user' in st.session_state:
                    st.session_state['current_user']['music_history'] = st.session_state['demo_music_history']
                
                return True
            else:
                # Real Firebase storage
                user_ref = self.db.collection('users').document(user_id)
                user_ref.update({
                    'music_history': firestore.ArrayUnion([music_entry])
                })
                return True
                
        except Exception as e:
            st.error(f"Error saving music data: {e}")
            return False
    
    def get_user_music_history(self, user_id):
        """Retrieve user's music generation history"""
        try:
            if st.session_state.get('firebase_demo'):
                return st.session_state.get('demo_music_history', [])
            else:
                user_doc = self.db.collection('users').document(user_id).get()
                if user_doc.exists:
                    return user_doc.to_dict().get('music_history', [])
                return []
                
        except Exception as e:
            st.error(f"Error retrieving music history: {e}")
            return []
    
    def update_user_preferences(self, user_id, preferences):
        """Update user preferences"""
        try:
            if st.session_state.get('firebase_demo'):
                st.session_state['demo_preferences'] = preferences
                if 'current_user' in st.session_state:
                    st.session_state['current_user']['preferences'] = preferences
                return True
            else:
                user_ref = self.db.collection('users').document(user_id)
                user_ref.update({'preferences': preferences})
                return True
                
        except Exception as e:
            st.error(f"Error updating preferences: {e}")
            return False
    
    def get_user_preferences(self, user_id):
        """Get user preferences"""
        try:
            if st.session_state.get('firebase_demo'):
                return st.session_state.get('demo_preferences', {
                    'favorite_mood': 'happy',
                    'preferred_tempo': 120,
                    'preferred_instruments': ['piano', 'guitar']
                })
            else:
                user_doc = self.db.collection('users').document(user_id).get()
                if user_doc.exists:
                    return user_doc.to_dict().get('preferences', {})
                return {}
                
        except Exception as e:
            st.error(f"Error retrieving preferences: {e}")
            return {}
    
    def logout_user(self):
        """Logout current user"""
        keys_to_remove = ['current_user', 'demo_user', 'demo_music_history', 'demo_preferences']
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
    
    def get_current_user(self):
        """Get current logged-in user"""
        return st.session_state.get('current_user', None)
    
    def is_user_logged_in(self):
        """Check if user is logged in"""
        return st.session_state.get('current_user') is not None

# Initialize Firebase Auth globally
firebase_auth = FirebaseAuth()
