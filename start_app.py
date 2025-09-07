import os
import subprocess
import sys
from pathlib import Path

def main():
    """
    Start the AI Job Assistant application.
    For Render deployment, this runs only the FastAPI backend.
    Streamlit frontend can be accessed separately or integrated.
    """
    
    # Set up environment
    port = int(os.environ.get("PORT", 10000))
    host = "0.0.0.0"
    
    # Ensure output directory exists
    output_dir = Path("backend/utils/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🚀 Starting AI Job Assistant on {host}:{port}")
    
    # For Render deployment, start FastAPI only
    if os.environ.get("RENDER"):
        print("📡 Render deployment detected - starting FastAPI backend only")
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "backend.app.main:app",
            "--host", host,
            "--port", str(port),
            "--workers", "1"
        ])
    else:
        # Local development - you can run both if needed
        print("💻 Local development - starting FastAPI backend")
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "backend.app.main:app",
            "--host", host,
            "--port", str(port),
            "--reload"
        ])

if __name__ == "__main__":
    main()