#!/bin/bash

# AI-Powered Job Assistant Deployment Script
echo "🚀 AI-Powered Job Assistant Deployment Setup"
echo "============================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys before deploying!"
    echo "   Required: GROQ_API_KEY"
    echo "   Optional: OPENAI_API_KEY"
    echo ""
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "🔧 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for deployment"
    echo "📌 Please add your remote repository:"
    echo "   git remote add origin <your-repo-url>"
    echo "   git push -u origin main"
    echo ""
fi

# Display deployment options
echo "🎯 Deployment Options:"
echo "1. Render (Recommended)"
echo "   - Push code to GitHub"
echo "   - Connect repository to Render"
echo "   - Use render.yaml for automatic deployment"
echo ""
echo "2. Docker (Local/Production)"
echo "   - Run: docker-compose up --build"
echo "   - Access: http://localhost:8501"
echo ""
echo "3. Manual Setup"
echo "   - Backend: cd backend && uvicorn app.main:app --reload"
echo "   - Frontend: streamlit run frontend/streamlit_app.py"
echo ""

# Check dependencies
echo "🔍 Checking dependencies..."
python --version
pip --version

echo ""
echo "✅ Deployment setup complete!"
echo "📖 See DEPLOYMENT.md for detailed instructions"
echo "🔗 Render Dashboard: https://dashboard.render.com"
