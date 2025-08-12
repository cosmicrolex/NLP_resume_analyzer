#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('stopwords', quiet=True); nltk.download('punkt', quiet=True)"

# Create output directory
mkdir -p utils/output

echo "Build completed successfully!"
