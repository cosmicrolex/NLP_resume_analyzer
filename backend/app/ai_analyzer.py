
# This module handles AI analysis, loading the API key from .env and sending the resume text (and optional job description) to Groq's API.

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Try to load environment variables from different possible locations
env_paths = [
    os.path.join(os.path.dirname(__file__), '..', '..', '.env'),  # Root directory
    os.path.join(os.path.dirname(__file__), '..', '.env'),        # Backend directory
    os.path.join(os.path.dirname(__file__), '.env'),              # Current directory
]

for env_path in env_paths:
    if os.path.exists(env_path):
        load_dotenv(env_path)
        break

# Get API key from environment variable
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set. Please set it in your environment or .env file.")

# Initialize Groq client (using OpenAI SDK compatibility)
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

def analyze_resume_with_ai(resume_text, job_description=None):
    """
    Analyze resume text using an AI model to identify deficiencies and provide improvement suggestions.
    
    Args:
        resume_text (str): Extracted resume text
        job_description (str, optional): Job description text for context
    
    Returns:
        dict: AI-generated insights or error message
    """
    try:
        # Define the base prompt
        prompt = """
        You are an expert career coach analyzing a resume to identify areas for improvement. Your task is to:
        - Identify missing or weak sections (e.g., skills, extracurricular activities, certifications, work experience).
        - Suggest specific improvements to make the resume stronger for job applications.
        - Highlight any critical gaps, such as missing technical skills, leadership experience, or relevant activities.
        - Provide concise, actionable advice for the candidate.

        Resume Text:
        {resume_text}

        {job_description_section}

        Output your response in a structured JSON format with the following keys:
        - deficiencies: List of identified weaknesses (e.g., ["Missing technical skills", "No extracurricular activities"]).
        - suggestions: List of specific improvement suggestions (e.g., ["Add Python and SQL skills", "Include volunteer work"]).
        - critical_gaps: List of critical missing elements that could prevent job success.
        """
        
        # Include job description if provided
        job_description_section = ""
        if job_description:
            job_description_section = f"Job Description for Context:\n{job_description}\n\nPlease tailor your analysis to align with the job description where relevant."

        # Format the prompt with dynamic inputs
        formatted_prompt = prompt.format(
            resume_text=resume_text,
            job_description_section=job_description_section
        )

        # Call the Groq API
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Use Groq's model
            messages=[
                {"role": "system", "content": "You are a professional career coach with expertise in resume analysis."},
                {"role": "user", "content": formatted_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # Parse and return the response as a dictionary
        response_content = response.choices[0].message.content
        try:
            # Try to parse as JSON first
            ai_insights = json.loads(response_content)
            return ai_insights
        except json.JSONDecodeError:
            # If JSON parsing fails, return a structured response
            return {
                "deficiencies": ["Unable to parse structured response"],
                "suggestions": ["Please check the AI model response format"],
                "critical_gaps": ["Response parsing error"],
                "raw_response": response_content
            }

    except Exception as e:
        print(f"DEBUG - AI analysis error: {str(e)}")
        return {"error": f"AI analysis failed: {str(e)}"}