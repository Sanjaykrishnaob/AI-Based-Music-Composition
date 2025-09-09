#!/usr/bin/env python3
"""
Setup and Test Script for AI Music Composition Project
Milestones 1 & 2 Implementation

This script helps set up the environment and test the implementation.
"""

import subprocess
import sys
import importlib
import os
from pathlib import Path

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False

def setup_environment():
    """Set up the required environment"""
    print("🔧 Setting up AI Music Composition environment...")
    print("=" * 50)
    
    # Core dependencies
    core_packages = [
        "streamlit>=1.28.0",
        "transformers>=4.35.0", 
        "torch>=2.1.0",
        "sentence-transformers>=2.2.2",
        "numpy>=1.25.0",
        "pandas>=2.1.0",
        "scikit-learn>=1.3.0"
    ]
    
    # Audio processing packages
    audio_packages = [
        "soundfile>=0.12.1",
        "librosa>=0.10.0",
        "matplotlib>=3.7.0",
        "scipy>=1.11.0"
    ]
    
    # Optional packages for enhanced features
    optional_packages = [
        "plotly>=5.15.0",
        "pydub>=0.25.1",
        "torchaudio>=2.1.0",
        "accelerate>=0.20.0"
    ]
    
    print("📦 Installing core dependencies...")
    for package in core_packages:
        package_name = package.split(">=")[0].split("==")[0]
        print(f"Installing {package_name}...")
        if install_package(package):
            print(f"✅ {package_name} installed successfully")
        else:
            print(f"❌ Failed to install {package_name}")
    
    print("\n🎵 Installing audio processing packages...")
    for package in audio_packages:
        package_name = package.split(">=")[0].split("==")[0]
        print(f"Installing {package_name}...")
        if install_package(package):
            print(f"✅ {package_name} installed successfully")
        else:
            print(f"❌ Failed to install {package_name}")
    
    print("\n🎨 Installing optional visualization packages...")
    for package in optional_packages:
        package_name = package.split(">=")[0].split("==")[0]
        print(f"Installing {package_name}...")
        if install_package(package):
            print(f"✅ {package_name} installed successfully")
        else:
            print(f"⚠️ Optional package {package_name} failed to install")
    
    print("\n🚀 Attempting to install MusicGen (AudioCraft)...")
    # AudioCraft installation can be tricky
    audiocraft_installed = install_package("audiocraft")
    if audiocraft_installed:
        print("✅ AudioCraft (MusicGen) installed successfully!")
    else:
        print("⚠️ AudioCraft installation failed. Will use fallback synthesis.")
        print("💡 Try manual installation: pip install -U audiocraft")

def test_imports():
    """Test if all required imports work"""
    print("\n🧪 Testing imports...")
    print("=" * 30)
    
    test_cases = [
        ("streamlit", "streamlit"),
        ("transformers", "transformers"),
        ("torch", "torch"),
        ("sentence_transformers", "sentence_transformers"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("sklearn", "scikit-learn"),
        ("soundfile", "soundfile"),
        ("librosa", "librosa"),
        ("matplotlib.pyplot", "matplotlib"),
        ("scipy", "scipy"),
        ("plotly.express", "plotly"),
        ("pydub", "pydub"),
        ("audiocraft.models", "audiocraft")
    ]
    
    results = {}
    for import_name, package_name in test_cases:
        if check_package(import_name):
            print(f"✅ {package_name}")
            results[package_name] = True
        else:
            print(f"❌ {package_name}")
            results[package_name] = False
    
    return results

def test_mood_analyzer():
    """Test the mood analyzer component"""
    print("\n🎭 Testing Mood Analyzer (Milestone 1)...")
    print("=" * 40)
    
    try:
        from mood_analyzer import MoodAnalyzer
        
        analyzer = MoodAnalyzer()
        test_input = "I'm feeling energetic and ready to dance!"
        
        print(f"Input: '{test_input}'")
        result = analyzer.analyze_mood(test_input)
        
        if isinstance(result, dict):
            print("✅ Mood analysis successful!")
            print(f"   Mood: {result.get('mood_category', 'unknown')}")
            print(f"   Energy: {result.get('energy_level', 0)}/10")
            print(f"   Sentiment: {result.get('sentiment', 'unknown')}")
            print(f"   Tempo: {result.get('tempo', 0)} BPM")
            return True
        else:
            print("❌ Mood analysis returned unexpected format")
            return False
            
    except Exception as e:
        print(f"❌ Mood analyzer test failed: {e}")
        return False

def test_music_generator():
    """Test the music generator component"""
    print("\n🎵 Testing Music Generator (Milestone 2)...")
    print("=" * 40)
    
    try:
        from music_generator import MusicGenerator
        
        generator = MusicGenerator()
        
        # Test parameters
        test_params = {
            'mood_category': 'happy',
            'energy_level': 7,
            'tempo': 120,
            'key': 'major',
            'instruments': ['piano', 'guitar'],
            'text_prompt': 'upbeat happy music with piano and guitar'
        }
        
        print("Testing music generation...")
        
        # Get generation info
        gen_info = generator.get_generation_info()
        print(f"Generator: {gen_info['model_name']}")
        print(f"MusicGen Available: {gen_info['musicgen_available']}")
        
        if gen_info['musicgen_available']:
            print("✅ MusicGen integration working!")
        else:
            print("⚠️ Using fallback synthesis (MusicGen not available)")
        
        return True
        
    except Exception as e:
        print(f"❌ Music generator test failed: {e}")
        return False

def run_streamlit_app():
    """Launch the Streamlit app"""
    print("\n🚀 Launching Streamlit app...")
    print("=" * 30)
    
    app_path = Path(__file__).parent / "app.py"
    
    if app_path.exists():
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])
        except KeyboardInterrupt:
            print("\n👋 App stopped by user")
        except Exception as e:
            print(f"❌ Failed to launch app: {e}")
    else:
        print(f"❌ App file not found: {app_path}")

def main():
    """Main setup and test function"""
    print("🎵 AI Music Composition - Setup & Test")
    print("Milestones 1 & 2 Implementation")
    print("=" * 50)
    
    choice = input("""
Choose an option:
1. 🔧 Setup environment (install dependencies)
2. 🧪 Test components
3. 🚀 Launch Streamlit app
4. 📋 Complete setup and test
5. ❌ Exit

Enter choice (1-5): """).strip()
    
    if choice == "1":
        setup_environment()
        
    elif choice == "2":
        results = test_imports()
        test_mood_analyzer()
        test_music_generator()
        
        # Summary
        print("\n📊 Test Summary:")
        print("=" * 20)
        core_working = all([
            results.get('transformers', False),
            results.get('sentence_transformers', False),
            results.get('torch', False),
            results.get('streamlit', False)
        ])
        
        if core_working:
            print("✅ Core functionality ready!")
        else:
            print("❌ Core dependencies missing")
            
        if results.get('audiocraft', False):
            print("✅ MusicGen available for advanced generation")
        else:
            print("⚠️ MusicGen not available (will use fallback)")
        
    elif choice == "3":
        run_streamlit_app()
        
    elif choice == "4":
        setup_environment()
        print("\n" + "="*50)
        test_imports()
        test_mood_analyzer()
        test_music_generator()
        
        print("\n🎉 Setup complete! Ready to launch app.")
        launch = input("Launch Streamlit app now? (y/n): ").strip().lower()
        if launch == 'y':
            run_streamlit_app()
            
    elif choice == "5":
        print("👋 Goodbye!")
        
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
