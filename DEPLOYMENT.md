# Deployment Guide for AI Job Assistant

## Docker Deployment on Render

This project is optimized for Docker deployment on Render with all dependencies properly configured.

### Files Created for Deployment:

1. **Dockerfile** - Comprehensive Docker configuration
2. **requirements.txt** - Python dependencies with compatible versions
3. **render.yaml** - Render service configuration
4. **start.sh** - Startup script with dependency checks
5. **.dockerignore** - Optimized build context
6. **runtime.txt** - Python version specification

### Render Configuration:

#### Option 1: Using render.yaml (Recommended)
1. Push all files to your GitHub repository
2. Connect your repository to Render
3. Render will automatically detect the `render.yaml` file
4. Set your environment variables:
   - `GROQ_API_KEY` - Your Groq API key
   - `OPENAI_API_KEY` - Your OpenAI API key (optional)

#### Option 2: Manual Configuration
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the following settings:
   - **Environment**: Docker
   - **Dockerfile Path**: ./Dockerfile
   - **Build Command**: (leave empty)
   - **Start Command**: (leave empty)
   - **Plan**: Starter or higher
   - **Region**: Choose your preferred region

### Environment Variables:
Set these in your Render dashboard:
```
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here (optional)
API_BASE_URL=https://your-app-name.onrender.com
```

### Features Included:

✅ **Python 3.11** - Better compatibility than 3.12/3.13
✅ **System Dependencies** - poppler-utils, tesseract-ocr for PDF processing
✅ **Build Tools** - gcc, g++, make for compiling packages
✅ **spaCy Model** - Automatically downloads en_core_web_sm
✅ **NLTK Data** - Downloads stopwords and punkt tokenizer
✅ **Health Check** - Built-in health monitoring
✅ **Optimized Build** - .dockerignore for faster builds
✅ **Error Handling** - Graceful fallbacks for missing dependencies

### Build Process:

1. **Base Image**: Python 3.11-slim for stability
2. **System Packages**: Install PDF/OCR dependencies
3. **Python Packages**: Install from requirements.txt with retries
4. **ML Models**: Download spaCy and NLTK data
5. **Startup**: Use start.sh for runtime checks

### Troubleshooting:

#### Build Fails:
- Check that all files are committed to your repository
- Ensure Dockerfile is in the root directory
- Verify requirements.txt has compatible versions

#### Runtime Errors:
- Check environment variables are set correctly
- Monitor logs for spaCy/NLTK download issues
- Verify health check endpoint: `/health`

#### PDF Processing Issues:
- System dependencies (poppler-utils, tesseract) are included
- OCR should work for image-based PDFs
- Check file upload size limits

### Local Testing:

Build and test locally:
```bash
# Build the Docker image
docker build -t ai-job-assistant .

# Run the container
docker run -p 10000:10000 \
  -e GROQ_API_KEY=your_key_here \
  ai-job-assistant

# Test the health endpoint
curl http://localhost:10000/health
```

### Performance Notes:

- **Single Worker**: Configured for Render's resource limits
- **Memory Efficient**: Optimized package versions
- **Fast Startup**: Pre-downloaded models in build phase
- **Health Monitoring**: Built-in health checks

### Support:

If deployment fails:
1. Check Render build logs for specific errors
2. Verify all environment variables are set
3. Ensure your repository has all the deployment files
4. Try clearing build cache and redeploying

The Docker configuration handles all dependencies automatically, making deployment reliable and consistent across environments.