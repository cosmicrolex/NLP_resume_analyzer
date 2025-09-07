import os
import subprocess
import sys
import threading
import time
from pathlib import Path

def start_fastapi():
    """Start FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "backend.app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--workers", "1"
    ])

def start_streamlit():
    """Start Streamlit frontend"""
    print("🎨 Starting Streamlit frontend...")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "frontend/streamlit_app.py",
        "--server.port", str(os.environ.get("PORT", 10000)),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.runOnSave", "false",
        "--browser.gatherUsageStats", "false"
    ])

def main():
    """
    Start the AI Job Assistant application.
    For Render deployment, this runs both FastAPI backend and Streamlit frontend.
    """
    
    # Set up environment
    port = int(os.environ.get("PORT", 10000))
    
    # Ensure output directory exists
    output_dir = Path("backend/utils/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🚀 Starting AI Job Assistant on port {port}")
    
    if os.environ.get("RENDER"):
        print("📡 Render deployment detected - starting both FastAPI backend and Streamlit frontend")
        
        # Start FastAPI in a separate thread
        fastapi_thread = threading.Thread(target=start_fastapi, daemon=True)
        fastapi_thread.start()
        
        # Give FastAPI time to start
        time.sleep(5)
        
        # Start Streamlit on the main thread (this will be the primary service)
        start_streamlit()
        
    else:
        print("💻 Local development - starting both services")
        
        # Start FastAPI in a separate thread
        fastapi_thread = threading.Thread(target=start_fastapi, daemon=True)
        fastapi_thread.start()
        
        # Give FastAPI time to start
        time.sleep(2)
        
        # Start Streamlit on the main thread
        start_streamlit()

if __name__ == "__main__":
    main()