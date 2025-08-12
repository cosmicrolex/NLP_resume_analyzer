# 🚀 Deployment Guide - AI-Powered Job Assistant

This guide covers deploying the AI-Powered Job Assistant on Render and other platforms.

## 📋 Prerequisites

1. **API Keys Required:**
   - Groq API Key (for LLM analysis)
   - OpenAI API Key (optional fallback)

2. **Accounts Needed:**
   - Render account (free tier available)
   - GitHub account (for code repository)

## 🎯 Render Deployment (Recommended)

### Option 1: Using render.yaml (Multi-Service)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Connect to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository containing your project

3. **Configure Environment Variables:**
   
   **For Backend Service:**
   - `GROQ_API_KEY`: Your Groq API key
   - `OPENAI_API_KEY`: Your OpenAI API key (optional)
   
   **For Frontend Service:**
   - `API_BASE_URL`: `https://ai-job-assistant-backend.onrender.com`

4. **Deploy:**
   - Render will automatically detect the `render.yaml` file
   - Both services will be deployed simultaneously
   - Wait for build completion (5-10 minutes)

### Option 2: Manual Service Creation

**Deploy Backend:**
1. Create new Web Service
2. Connect GitHub repository
3. Configure:
   - **Build Command:** `cd backend && chmod +x build.sh && ./build.sh`
   - **Start Command:** `cd backend/app && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Add API keys

**Deploy Frontend:**
1. Create new Web Service
2. Connect same GitHub repository
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run frontend/streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --server.enableCORS false --server.enableXsrfProtection false`
   - **Environment:** Add `API_BASE_URL` pointing to backend

## 🐳 Docker Deployment

### Local Development

1. **Create .env file:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access Services:**
   - Backend: http://localhost:8000
   - Frontend: http://localhost:8501

### Production Docker

**Build Images:**
```bash
# Backend
docker build -t ai-job-assistant-backend ./backend

# Frontend  
docker build -t ai-job-assistant-frontend ./frontend
```

**Run Containers:**
```bash
# Backend
docker run -d -p 8000:8000 \
  -e GROQ_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  ai-job-assistant-backend

# Frontend
docker run -d -p 8501:8501 \
  -e API_BASE_URL=http://backend:8000 \
  ai-job-assistant-frontend
```

## ☁️ Alternative Platforms

### Heroku

1. **Create Procfile for Backend:**
   ```
   web: cd backend/app && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. **Create Procfile for Frontend:**
   ```
   web: streamlit run frontend/streamlit_app.py --server.port $PORT --server.address 0.0.0.0
   ```

3. **Deploy:**
   ```bash
   heroku create your-app-backend
   heroku create your-app-frontend
   heroku config:set GROQ_API_KEY=your_key
   git push heroku main
   ```

### Railway

1. **Connect GitHub repository**
2. **Configure environment variables**
3. **Deploy automatically**

### Vercel (Frontend Only)

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy:**
   ```bash
   cd frontend
   vercel --prod
   ```

## 🔧 Configuration Details

### Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `GROQ_API_KEY` | Groq API key for LLM | Yes | `gsk_...` |
| `OPENAI_API_KEY` | OpenAI API key (fallback) | No | `sk-...` |
| `API_BASE_URL` | Backend URL for frontend | Yes | `https://api.example.com` |

### Service Configuration

**Backend Requirements:**
- Python 3.11+
- 512MB RAM minimum
- NLTK data download during build
- PDF processing capabilities

**Frontend Requirements:**
- Python 3.11+
- 256MB RAM minimum
- Streamlit server configuration
- CORS disabled for API calls

## 🔍 Troubleshooting

### Common Issues

**1. Build Failures:**
```bash
# Check Python version
python --version

# Verify requirements
pip install -r requirements.txt

# Test NLTK download
python -c "import nltk; nltk.download('stopwords')"
```

**2. API Connection Issues:**
```bash
# Test backend health
curl https://your-backend.onrender.com/

# Check environment variables
echo $API_BASE_URL
```

**3. Memory Issues:**
- Upgrade to paid plan for more RAM
- Optimize requirements.txt
- Use lighter ML models

### Logs and Monitoring

**Render:**
- View logs in Render dashboard
- Monitor resource usage
- Set up health checks

**Docker:**
```bash
# View logs
docker logs container_name

# Monitor resources
docker stats
```

## 📊 Performance Optimization

### Backend Optimization

1. **Caching:**
   - Implement Redis for TF-IDF results
   - Cache LLM responses

2. **Database:**
   - Add PostgreSQL for user data
   - Store analysis history

3. **Scaling:**
   - Use multiple workers
   - Implement load balancing

### Frontend Optimization

1. **Streamlit Configuration:**
   ```python
   st.set_page_config(
       page_title="AI Job Assistant",
       layout="wide",
       initial_sidebar_state="expanded"
   )
   ```

2. **Caching:**
   ```python
   @st.cache_data
   def load_data():
       # Cache expensive operations
       pass
   ```

## 🔐 Security Considerations

1. **API Keys:**
   - Never commit to repository
   - Use environment variables
   - Rotate keys regularly

2. **CORS:**
   - Configure properly for production
   - Whitelist specific domains

3. **File Upload:**
   - Validate file types
   - Limit file sizes
   - Scan for malware

## 📈 Monitoring and Analytics

1. **Health Checks:**
   - Implement `/health` endpoint
   - Monitor uptime

2. **Analytics:**
   - Track usage metrics
   - Monitor API response times
   - Log errors and exceptions

3. **Alerts:**
   - Set up error notifications
   - Monitor resource usage
   - Track API rate limits

## 🚀 Next Steps

After successful deployment:

1. **Test all features:**
   - Resume upload and analysis
   - Job description matching
   - LLM insights generation

2. **Monitor performance:**
   - Check response times
   - Monitor error rates
   - Track resource usage

3. **Scale as needed:**
   - Upgrade plans for more traffic
   - Add caching layers
   - Implement CDN for static assets

---

**Need Help?**
- Check the logs first
- Verify environment variables
- Test API endpoints manually
- Contact support if issues persist
