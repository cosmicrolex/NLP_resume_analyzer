#!/bin/bash
set -e

echo "🔧 Starting backend build for Render..."

# Upgrade pip and install build tools
echo "📦 Installing build tools..."
python -m pip install --upgrade pip
pip install setuptools==68.2.2 wheel==0.41.2

# Install dependencies without binary restrictions
echo "📦 Installing dependencies..."
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install python-multipart==0.0.6
pip install python-dotenv==1.0.0
pip install openai==1.3.7
pip install requests==2.31.0
pip install pydantic==2.5.0
pip install python-dateutil==2.8.2
pip install pypdf2==3.0.1
pip install pdfplumber==0.10.3
pip install nltk==3.8.1

# Install ML packages with specific versions
echo "📦 Installing ML packages..."
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install scikit-learn==1.2.2

# Download NLTK data
echo "📚 Downloading NLTK data..."
python -c "import nltk; nltk.download('stopwords', quiet=True); nltk.download('punkt', quiet=True)"

# Create output directory
echo "📁 Creating output directory..."
mkdir -p utils/output

echo "✅ Backend build completed successfully!"
