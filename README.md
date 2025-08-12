AI-Powered Job Assistant
This project is a job description and resume analyzer that takes inputs of job descriptions from recruiters and resumes from candidates, analyzes the text using TF-IDF and cosine similarity for matching, and provides AI-powered insights to improve resumes. It uses a FastAPI backend for processing and a Streamlit frontend for user interaction.
UPDATE LOG
27-July-2025

Added AI-powered resume analysis using OpenAI's API to identify deficiencies (e.g., missing skills, extracurricular activities) and provide improvement suggestions.
Created backend/app/ai_analyzer.py to handle AI interactions.
Updated backend/app/main.py to include AI insights in /analyze-resume/, /match-resume-job/, and /match-resume-job-pdf/ endpoints.
Modified frontend/streamlit_app.py to display AI insights in the "Resume Analysis" and "Resume-Job Matching" pages.
Added .env file support for securely storing the OpenAI API key.

30-June-2025

Added tfidf_analyzer.py to implement TF-IDF and calculate word importance probabilities.

11-June-2025

Programmed pdf_parser.py to extract text from PDF files, storing it in a text file when run from VS Code terminal.
Configured FastAPI to display extracted text in JSON format in the browser.

Prerequisites

Python 3.8+
Virtual environment
OpenAI API key (stored in backend/.env)

Setup Instructions

Clone the repository:git clone <repository-url>

Create and activate a virtual environment:python -m venv virtualenvironment
cd .\AI-Powered-Job-Assistant\virtualenvironment\Scripts\
.\activate

Install dependencies:
Copy requirements.txt from the root directory to virtualenvironment\Scripts\.
Run:pip install -r requirements.txt

Navigate to backend/ and install backend-specific dependencies:cd .\AI-Powered-Job-Assistant\backend\
pip install -r requirements.txt

Create a .env file in backend/ with your OpenAI API key:OPENAI_API_KEY=your_openai_api_key_here

Place a sample PDF resume in backend/utils/ for testing.

Running the Backend

Navigate to the backend app directory:cd .\AI-Powered-Job-Assistant\backend\app

Start the FastAPI server:uvicorn app.main:app --reload

Access the API at http://127.0.0.1:8000.

Running the Frontend

Open a new terminal and navigate to the frontend directory:cd .\AI-Powered-Job-Assistant\frontend

Start the Streamlit app:streamlit run streamlit_app.py

Access the frontend at http://localhost:8501.

Testing the API

Analyze Resume:
curl.exe -X POST -F "file=@path\to\your_resume.pdf" http://127.0.0.1:8000/analyze-resume/

In Postman, select POST, set the endpoint to http://127.0.0.1:8000/analyze-resume/, choose form-data, set key as file, and upload the PDF.
Response includes extracted text, TF-IDF analysis, and AI insights.

Match Resume with Job Description:
curl.exe -X POST -F "file=@path\to\your_resume.pdf" -F "job_description=your job description text" http://127.0.0.1:8000/match-resume-job/

In Postman, add job_description as a form-data key with the text value.

Match Resume with Job Description PDF:
curl.exe -X POST -F "file=@path\to\your_resume.pdf" -F "jd_file=@path\to\your_job_description.pdf" http://127.0.0.1:8000/match-resume-job-pdf/

Features

PDF Text Extraction: Extracts text from resume and job description PDFs.
TF-IDF Analysis: Identifies key terms and their importance in resumes and job descriptions.
Cosine Similarity: Measures compatibility between resumes and job descriptions.
AI Insights: Uses OpenAI's API to identify resume deficiencies (e.g., missing skills, extracurriculars) and provide tailored improvement suggestions.
Streamlit Frontend: User-friendly interface with dark/light mode, displaying analysis results and AI insights.

## 🚀 Deployment

### Quick Deploy to Render

1. **Push to GitHub:**

   ```bash
   git add .
   git commit -m "Deploy to Render"
   git push origin main
   ```

2. **Deploy on Render:**

   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Set environment variables:
     - `GROQ_API_KEY`: Your Groq API key
     - `API_BASE_URL`: Backend service URL

3. **Access Your App:**
   - Backend: `https://ai-job-assistant-backend.onrender.com`
   - Frontend: `https://ai-job-assistant-frontend.onrender.com`

### Docker Deployment

```bash
# Run deployment setup
./deploy.sh

# Start with Docker Compose
docker-compose up --build
```

### Environment Variables

Create `.env` file with:

```
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
API_BASE_URL=http://127.0.0.1:8000
```

📖 **See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions**

Notes

Ensure the PDF file names match those used in API calls.
The .env file should not be committed to version control; add it to .gitignore.
For alternative AI models (e.g., Grok, Gemini), update ai_analyzer.py with the respective API client and endpoint.
