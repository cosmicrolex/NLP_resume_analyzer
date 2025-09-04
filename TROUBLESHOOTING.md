# Troubleshooting Guide

## HTTPSConnectionPool Timeout Error Resolution

### Problem Description
The error `HTTPSConnectionPool(host='ai-job-assistant.onrender.com', port=443): Read timed out. (read timeout=30)` occurs when the Streamlit frontend tries to connect to the external Render URL instead of the local FastAPI backend running in the same container.

### Root Cause Analysis

1. **Architecture Mismatch**: The application was designed to run both Streamlit (port 10000) and FastAPI (port 8000) simultaneously, but the Dockerfile was only starting the FastAPI backend.

2. **Frontend Configuration**: The Streamlit app was trying to connect to the external URL (`https://ai-job-assistant.onrender.com`) instead of the local FastAPI instance.

3. **Deployment Configuration**: The Render deployment was only running the FastAPI backend, not the full application with both services.

### Solution Implemented

#### 1. Updated Dockerfile
**File**: `Dockerfile`
**Change**: Modified the CMD instruction to use the start script that runs both services:
```dockerfile
# Before
CMD uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT --workers 1

# After  
CMD ["python", "start_app.py"]
```

#### 2. Updated Frontend Configuration
**File**: `frontend/streamlit_app.py`
**Changes**:
- Added environment detection to use local backend when running in production
- Implemented fallback URL mechanism for connection testing
- Updated API base URL logic:

```python
# Check if we're running in production (Render) or locally
if os.getenv("RENDER"):
    # In production, both services run in the same container
    API_BASE_URL = "http://localhost:8000"
else:
    # For local development, try environment variable or default to localhost
    API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# Fallback URLs to try if the primary URL fails
FALLBACK_URLS = [
    "https://ai-job-assistant.onrender.com",
    "https://nlp-ai-resume-analysis.onrender.com", 
    "https://ai-powered-job-assistant.onrender.com"
]
```

#### 3. Updated Render Configuration
**File**: `render.yaml`
**Change**: Added RENDER environment variable to identify production environment:
```yaml
envVars:
  - key: RENDER
    value: "true"
```

### How the Solution Works

1. **Production Environment**: When deployed on Render, the `RENDER` environment variable is set, causing the frontend to connect to `http://localhost:8000` (the local FastAPI backend).

2. **Local Development**: When running locally, the frontend uses the `API_BASE_URL` environment variable or defaults to `http://127.0.0.1:8000`.

3. **Fallback Mechanism**: If the primary connection fails, the application tries alternative URLs and provides detailed error information.

4. **Unified Deployment**: Both Streamlit and FastAPI services run in the same container, eliminating network connectivity issues.

### Testing the Fix

1. **Backend Connection Test**: Use the "Test Backend Connection" button in the Streamlit sidebar to verify connectivity.

2. **Health Check**: The `/health` endpoint provides system status and available endpoints.

3. **Error Handling**: Detailed error information is displayed when connections fail, helping with debugging.

### Additional Improvements

1. **Enhanced Error Handling**: Comprehensive error messages with troubleshooting suggestions.

2. **Connection Retry Logic**: Automatic fallback to alternative URLs if the primary connection fails.

3. **Environment Detection**: Smart detection of production vs. development environments.

4. **Debugging Tools**: Built-in connection testing and health monitoring.

### Prevention Measures

1. **Environment Variables**: Always set appropriate environment variables for different deployment environments.

2. **Health Checks**: Implement health check endpoints for monitoring service status.

3. **Connection Testing**: Include built-in tools for testing API connectivity.

4. **Documentation**: Maintain clear documentation of the application architecture and deployment process.

### Common Issues and Solutions

#### Issue: Connection still fails after deployment
**Solution**: 
- Check Render logs for startup errors
- Verify environment variables are set correctly
- Ensure both services are starting properly

#### Issue: Local development not working
**Solution**:
- Set `API_BASE_URL=http://127.0.0.1:8000` in your local `.env` file
- Run both services using `python start_app.py`

#### Issue: Timeout errors persist
**Solution**:
- Increase timeout values in the `make_api_request` function
- Check if the backend service is responding to health checks
- Verify firewall and network settings

### Monitoring and Maintenance

1. **Regular Health Checks**: Monitor the `/health` endpoint for service status.

2. **Log Monitoring**: Check Render logs for any startup or runtime errors.

3. **Performance Monitoring**: Monitor response times and connection success rates.

4. **Environment Variable Management**: Keep environment variables up to date and secure.

This solution ensures reliable communication between the frontend and backend services while providing robust error handling and debugging capabilities.