#!/bin/bash

# Startup script for the AI Job Assistant
set -e

echo "🚀 Starting AI Job Assistant..."

# Ensure output directory exists
mkdir -p backend/utils/output

# Check if spaCy model is available
echo "🧠 Checking spaCy model..."
python -c "
import spacy
try:
    nlp = spacy.load('en_core_web_sm')
    print('✅ spaCy model is available')
except OSError:
    print('⚠️ spaCy model not found, downloading...')
    import subprocess
    import sys
    subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'])
    print('✅ spaCy model downloaded successfully')
"

# Check NLTK data
echo "📚 Checking NLTK data..."
python -c "
import nltk
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    print('✅ NLTK data is available')
except LookupError:
    print('⚠️ NLTK data not found, downloading...')
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    print('✅ NLTK data downloaded successfully')
"

echo "✅ All dependencies are ready!"

# Start the application
echo "🌟 Starting FastAPI server..."
exec uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-10000} --workers 1