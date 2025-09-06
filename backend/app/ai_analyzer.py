
# This module handles AI analysis, dynamically using user-provided GROQ API keys

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Optional: Try to load environment variables as fallback (but don't require them)
env_paths = [
    os.path.join(os.path.dirname(__file__), '..', '..', '.env'),  # Root directory
    os.path.join(os.path.dirname(__file__), '..', '.env'),        # Backend directory
    os.path.join(os.path.dirname(__file__), '.env'),              # Current directory
]

for env_path in env_paths:
    if os.path.exists(env_path):
        load_dotenv(env_path)
        break

def analyze_resume_with_ai(resume_text, job_description=None, groq_api_key=None):
    """
    Analyze resume text using an AI model to identify deficiencies and provide improvement suggestions.
    
    Args:
        resume_text (str): Extracted resume text
        job_description (str, optional): Job description text for context
        groq_api_key (str): User-provided GROQ API key for dynamic authentication
    
    Returns:
        dict: AI-generated insights or error message
    """
    # Validate API key
    if not groq_api_key:
        raise ValueError("GROQ API key is required. Please provide your API key.")
    
    # Initialize Groq client with user-provided API key
    try:
        client = OpenAI(
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1"
        )
    except Exception as e:
        raise ValueError(f"Failed to initialize GROQ client: {str(e)}")
    
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

        IMPORTANT: You MUST respond with a valid JSON object in exactly this format:
        {{
            "deficiencies": ["weakness 1", "weakness 2", "weakness 3"],
            "suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"],
            "critical_gaps": ["gap 1", "gap 2", "gap 3"]
        }}

        Do not include any text before or after the JSON object. Only return the JSON.
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
                {"role": "system", "content": "You are a professional career coach with expertise in resume analysis. Always respond with valid JSON format only, no additional text."},
                {"role": "user", "content": formatted_prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent JSON output
            max_tokens=1000
        )

        # Parse and return the response as a dictionary
        response_content = response.choices[0].message.content.strip()
        
        # Clean up the response content to extract JSON
        if response_content.startswith('```json'):
            response_content = response_content.replace('```json', '').replace('```', '').strip()
        elif response_content.startswith('```'):
            response_content = response_content.replace('```', '').strip()
        
        try:
            # Try to parse as JSON first
            ai_insights = json.loads(response_content)
            
            # Validate that required keys exist
            if not isinstance(ai_insights, dict):
                raise ValueError("Response is not a dictionary")
            
            # Ensure all required keys exist with default values
            ai_insights.setdefault("deficiencies", ["No significant deficiencies identified"])
            ai_insights.setdefault("suggestions", ["Continue developing existing skills"])
            ai_insights.setdefault("critical_gaps", ["No critical gaps identified"])
            
            return ai_insights
            
        except (json.JSONDecodeError, ValueError) as e:
            # If JSON parsing fails, try to extract useful information from the text
            print(f"JSON parsing failed: {str(e)}")
            print(f"Raw response: {response_content}")
            
            # Try to create a structured response from unstructured text
            lines = response_content.split('\n')
            deficiencies = []
            suggestions = []
            critical_gaps = []
            
            current_section = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Check for section headers
                if any(keyword in line.lower() for keyword in ['deficienc', 'weakness', 'weak']):
                    current_section = 'deficiencies'
                    continue
                elif any(keyword in line.lower() for keyword in ['suggestion', 'improve', 'recommend']):
                    current_section = 'suggestions'
                    continue
                elif any(keyword in line.lower() for keyword in ['critical', 'gap', 'missing']):
                    current_section = 'critical_gaps'
                    continue
                
                # Extract bullet points or numbered items
                if line.startswith(('-', '•', '*')) or line[0:2].strip().isdigit():
                    cleaned_line = line.lstrip('-•*0123456789. ').strip()
                    if cleaned_line:
                        if current_section == 'deficiencies':
                            deficiencies.append(cleaned_line)
                        elif current_section == 'suggestions':
                            suggestions.append(cleaned_line)
                        elif current_section == 'critical_gaps':
                            critical_gaps.append(cleaned_line)
            
            # If we couldn't extract structured data, provide the raw response
            if not deficiencies and not suggestions and not critical_gaps:
                return {
                    "deficiencies": ["AI response could not be parsed properly"],
                    "suggestions": ["Please try again or check your API key"],
                    "critical_gaps": ["Response parsing failed"],
                    "raw_response": response_content
                }
            
            return {
                "deficiencies": deficiencies if deficiencies else ["No specific deficiencies identified"],
                "suggestions": suggestions if suggestions else ["Continue professional development"],
                "critical_gaps": critical_gaps if critical_gaps else ["No critical gaps identified"],
                "raw_response": response_content
            }

    except Exception as e:
        print(f"DEBUG - AI analysis error: {str(e)}")
        return {"error": f"AI analysis failed: {str(e)}"}