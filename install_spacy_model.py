#!/usr/bin/env python3
"""
Script to download spaCy English model after spaCy installation.
This avoids build timeout issues on Render.
"""
import subprocess
import sys

def install_spacy_model():
    try:
        print("Downloading spaCy English model...")
        subprocess.check_call([
            sys.executable, "-m", "spacy", "download", "en_core_web_sm"
        ])
        print("✅ spaCy model installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install spaCy model: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = install_spacy_model()
    sys.exit(0 if success else 1)