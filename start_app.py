import threading
import subprocess
import os

def run_streamlit():
    # Start Streamlit on port 10000 (Render's required port)
    subprocess.run(["streamlit", "run", "frontend/streamlit_app.py", "--server.port", "10000", "--server.address", "0.0.0.0"])

def run_fastapi():
    # Start FastAPI with uvicorn on port 8000
    subprocess.run(["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"])

if __name__ == "__main__":
    # Start both servers in separate threads
    streamlit_thread = threading.Thread(target=run_streamlit)
    fastapi_thread = threading.Thread(target=run_fastapi)
    
    streamlit_thread.start()
    fastapi_thread.start()
    
    streamlit_thread.join()
    fastapi_thread.join()