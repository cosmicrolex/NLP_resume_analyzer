#!/bin/bash

# Build script for Render native Python deployment
set -o errexit  # Exit on error

echo "🚀 Starting build process..."

# Upgrade pip
python -m pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install -r requirements.txt

# Download spaCy model
echo "🧠 Installing spaCy English model..."
python install_spacy_model.py

# Download NLTK data
echo "📚 Downloading NLTK data..."
python -c "
import nltk
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    print('✅ NLTK data downloaded successfully')
except Exception as e:
    print(f'⚠️ NLTK download warning: {e}')
"

echo "✅ Build completed successfully!"