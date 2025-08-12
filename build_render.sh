#!/bin/bash
set -e

echo "🔧 Starting frontend build for Render..."

# Upgrade pip and install build tools
echo "📦 Installing build tools..."
python -m pip install --upgrade pip
pip install setuptools==68.2.2 wheel==0.41.2

# Install dependencies one by one
echo "📦 Installing dependencies..."
pip install streamlit==1.28.1
pip install requests==2.31.0
pip install altair==5.1.2
pip install python-dateutil==2.8.2
pip install numpy==1.24.3
pip install pandas==2.0.3

echo "✅ Frontend build completed successfully!"
