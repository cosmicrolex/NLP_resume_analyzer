#!/bin/bash
set -e

echo "🔧 Starting frontend build for Render..."

# Upgrade pip and install build tools first
echo "📦 Installing build tools..."
python -m pip install --upgrade pip
python -m pip install setuptools>=65.0.0 wheel>=0.38.0

# Try to install with wheels first, fallback to source if needed
echo "📦 Installing dependencies..."
pip install --only-binary=:all: -r requirements.txt || {
    echo "⚠️  Wheel installation failed, trying source installation..."
    pip install -r requirements.txt
}

echo "✅ Frontend build completed successfully!"
