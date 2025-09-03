# Render Deployment Instructions

## IMPORTANT: Force Docker Deployment

Render is still using Python 3.13 instead of Docker. Follow these steps exactly:

### Step 1: Render Dashboard Settings

1. Go to your Render dashboard
2. Delete the existing service if it exists
3. Create a **NEW** Web Service
4. Connect your GitHub repository

### Step 2: Service Configuration

**CRITICAL**: Set these exact settings:

- **Environment**: `Docker` (NOT Python)
- **Dockerfile Path**: `./Dockerfile`
- **Build Command**: Leave EMPTY (delete any existing command)
- **Start Command**: Leave EMPTY (delete any existing command)
- **Branch**: `main` (or your default branch)

### Step 3: Environment Variables

Add these environment variables:
```
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
PORT=10000
```

### Step 4: Advanced Settings

- **Plan**: Starter or higher
- **Region**: Choose your preferred region
- **Auto-Deploy**: Yes

### Step 5: Deploy

1. Click "Create Web Service"
2. Render should now use Docker and Python 3.11
3. Monitor the build logs - you should see Docker commands, not pip install

### Troubleshooting

If you still see Python 3.13 errors:

1. **Delete the service completely**
2. **Clear browser cache**
3. **Create a brand new service**
4. **Double-check Environment is set to "Docker"**
5. **Ensure Build/Start commands are EMPTY**

### Verification

Once deployed successfully:
- Check `/health` endpoint returns 200 OK
- Upload a test PDF to verify functionality
- Monitor logs for any spaCy/NLTK issues

### Files in Repository

Make sure these files are committed:
- ✅ Dockerfile (Python 3.11)
- ✅ requirements.txt (minimal dependencies)
- ✅ render.yaml (Docker configuration)
- ✅ start.sh (startup script)
- ✅ .dockerignore (build optimization)

The key is ensuring Render uses Docker environment, not native Python.