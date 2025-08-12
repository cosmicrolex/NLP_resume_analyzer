import re
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
from openai import OpenAI
from dotenv import load_dotenv
from .simple_tfidf import SimpleTFIDF

# Load environment variables from root directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# Initialize Groq client (uses OpenAI SDK compatibility)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Download NLTK data
nltk.download('stopwords')
nltk.download('punkt')

def preprocess_text(text):
    """Minimal preprocessing to preserve meaningful terms"""
    if not text or not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove special characters but keep letters, numbers, spaces, and hyphens
    text = re.sub(r'[^a-zA-Z0-9\s\-]', ' ', text)
    
    # Remove standalone years (2020, 2021, etc.)
    text = re.sub(r'\b(19|20)\d{2}\b', '', text)
    
    # Remove very short words (less than 2 chars) and very long words (more than 20 chars)
    words = text.split()
    words = [word for word in words if 2 <= len(word) <= 20]
    
    # Minimal stopword removal - only remove very common words
    minimal_stopwords = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
        'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above',
        'below', 'between', 'among', 'this', 'that', 'these', 'those', 'is', 'was', 'are',
        'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall'
    }
    
    # Keep technical and meaningful terms
    filtered_words = [word for word in words if word not in minimal_stopwords]
    
    result = ' '.join(filtered_words)
    print(f"DEBUG - Preprocessed text preview: {result[:200]}...")  # Debug output
    return result

def analyze_resume_with_tfidf(resume_text):
    try:
        print(f"DEBUG - Original resume text length: {len(resume_text)}")

        # Initialize our custom TF-IDF analyzer
        tfidf_analyzer = SimpleTFIDF()

        # Get top keywords using our custom implementation
        keyword_scores = tfidf_analyzer.get_top_keywords(resume_text, top_n=20)

        print(f"DEBUG - Resume features found: {len(keyword_scores)}")
        print(f"DEBUG - Top resume features: {list(keyword_scores.keys())[:10]}")

        # Prepare top keywords for display
        top_keywords = []
        for term, score in keyword_scores.items():
            top_keywords.append({
                "term": term,
                "score": round(score, 4)
            })

        # LLM analysis for strengths and weaknesses
        llm_analysis = None
        if os.getenv("GROQ_API_KEY"):
            try:
                llm_analysis = get_resume_strengths_weaknesses(resume_text, keyword_scores)
                print(f"DEBUG - LLM analysis result: {llm_analysis}")
            except Exception as e:
                print(f"DEBUG - LLM strengths/weaknesses error: {str(e)}")
                import traceback
                print(f"DEBUG - Full traceback: {traceback.format_exc()}")
                llm_analysis = {"error": f"LLM analysis failed: {str(e)}"}

        return {
            "top_keywords": top_keywords,
            "llm_strengths_weaknesses": llm_analysis
        }
    except Exception as e:
        print(f"DEBUG - Resume analysis error: {str(e)}")
        return {"error": f"TF-IDF analysis failed: {str(e)}"}

def get_resume_strengths_weaknesses(resume_text, tfidf_scores):
    """Use Groq LLM to identify resume strengths and weaknesses."""
    top_terms = ", ".join([f"{term}: {score:.4f}" for term, score in sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:10]])
    system_prompt = (
        "You are a career advisor. Analyze the provided resume text. Identify 3-5 key strengths (e.g., specific skills, experiences, achievements) "
        f"and 3-5 weaknesses (e.g., gaps in experience, missing skills, unclear sections). Use the top TF-IDF keywords for context: {top_terms}. "
        "Return the response in JSON format: {\"strengths\": [\"bullet1\", \"bullet2\", ...], \"weaknesses\": [\"bullet1\", \"bullet2\", ...]}."
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": resume_text[:4000]}  # Truncate for token limits
        ],
        temperature=0.7,
        max_tokens=500
    )

    response_content = response.choices[0].message.content
    try:
        # Remove markdown code blocks if present
        if response_content.startswith("```json"):
            response_content = response_content.replace("```json", "").replace("```", "").strip()
        elif response_content.startswith("```"):
            response_content = response_content.replace("```", "").strip()

        # Extract JSON from the response (look for first { to last })
        start_idx = response_content.find('{')
        end_idx = response_content.rfind('}')
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_content = response_content[start_idx:end_idx+1]
            return json.loads(json_content)

        # Try to parse the entire content as JSON
        return json.loads(response_content)
    except json.JSONDecodeError:
        # If JSON parsing fails, return structured response
        return {
            "strengths": ["Unable to parse structured response"],
            "weaknesses": ["Please check the AI model response format"],
            "raw_response": response_content
        }

def analyze_job_description_with_tfidf(job_description_text):
    try:
        print(f"DEBUG - Original job desc text length: {len(job_description_text)}")
        processed_text = preprocess_text(job_description_text)
        print(f"DEBUG - Processed job desc text length: {len(processed_text)}")
        
        if not processed_text.strip():
            return {"error": "No valid text extracted for TF-IDF analysis"}

        vectorizer = TfidfVectorizer(
            max_features=50,
            ngram_range=(1, 2),
            min_df=1,
            max_df=1.0,
            stop_words=None,
            token_pattern=r'\b[a-zA-Z][a-zA-Z0-9]*\b'
        )
        
        tfidf_matrix = vectorizer.fit_transform([processed_text])
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]
        
        print(f"DEBUG - Job desc features found: {len(feature_names)}")
        print(f"DEBUG - Top job desc features: {feature_names[:10]}")
        
        keyword_scores = {feature_names[i]: tfidf_scores[i] for i in range(len(feature_names))}
        top_keywords = sorted(keyword_scores.items(), key=lambda x: x[1], reverse=True)[:15]
        
        return {
            "top_keywords": [{"term": term, "score": round(score, 4)} for term, score in top_keywords if score > 0]
        }
    except Exception as e:
        print(f"DEBUG - Job desc analysis error: {str(e)}")
        return {"error": f"TF-IDF analysis failed: {str(e)}"}

def calculate_resume_job_similarity(resume_text, job_description_text):
    try:
        print("DEBUG - Starting similarity calculation...")

        if not resume_text.strip() or not job_description_text.strip():
            return {"error": "One or both texts are empty"}

        # Initialize our custom TF-IDF analyzer
        tfidf_analyzer = SimpleTFIDF()

        # Compare documents using our custom implementation
        similarity_result = tfidf_analyzer.compare_documents(resume_text, job_description_text)

        similarity_score = similarity_result["similarity_score"]
        common_keywords = similarity_result["common_keywords"]

        print(f"DEBUG - Raw similarity score: {similarity_score}")
        print(f"DEBUG - Common terms found: {len(common_keywords)}")

        common_terms = common_keywords[:15]  # Top 15 common keywords
        
        # Match quality
        if similarity_score >= 0.3:
            match_quality = "Excellent Match"
        elif similarity_score >= 0.2:
            match_quality = "Good Match"
        elif similarity_score >= 0.1:
            match_quality = "Fair Match"
        else:
            match_quality = "Poor Match"
        
        return {
            "similarity_score": round(similarity_score, 4),
            "match_quality": match_quality,
            "common_keywords": common_terms,
            "total_features": len(common_terms)
        }
        
    except Exception as e:
        print(f"DEBUG - Similarity calculation error: {str(e)}")
        return {"error": f"Similarity calculation failed: {str(e)}"}

def comprehensive_resume_job_analysis(resume_text, job_description_text):
    try:
        print("DEBUG - Starting comprehensive analysis...")
        resume_analysis = analyze_resume_with_tfidf(resume_text)
        job_desc_analysis = analyze_job_description_with_tfidf(job_description_text)
        similarity_analysis = calculate_resume_job_similarity(resume_text, job_description_text)
        
        # LLM analysis for job fit
        llm_fit = None
        if os.getenv("GROQ_API_KEY"):
            try:
                llm_fit = get_resume_job_fit(resume_text, job_description_text, similarity_analysis)
            except Exception as e:
                print(f"DEBUG - LLM fit assessment error: {str(e)}")
                llm_fit = {"error": f"LLM fit assessment failed: {str(e)}"}
        
        return {
            "resume_analysis": resume_analysis,
            "job_description_analysis": job_desc_analysis,
            "similarity_analysis": similarity_analysis,
            "llm_fit_assessment": llm_fit
        }
        
    except Exception as e:
        print(f"DEBUG - Comprehensive analysis error: {str(e)}")
        return {"error": f"Comprehensive analysis failed: {str(e)}"}

def get_resume_job_fit(resume_text, job_description_text, similarity_analysis):
    """Use Groq LLM to assess resume fit for the job description."""
    sim_score = similarity_analysis.get("similarity_score", 0)
    common_terms_str = ", ".join([f"{kw['term']}: {kw['combined_importance']:.4f}" for kw in similarity_analysis.get("common_keywords", [])[:5]])
    system_prompt = (
        f"You are a hiring manager. Assess how well the provided resume fits the job description, considering the cosine similarity score ({sim_score}) "
        f"and top common keywords ({common_terms_str}). Provide: 1. Estimated fit percentage (0-100%). 2. 3-5 reasons why the resume fits well. "
        "3. 3-5 suggestions for improving the resume to better match the job. Return the response in JSON format: "
        "{\"fit_percentage\": int, \"reasons\": [\"bullet1\", \"bullet2\", ...], \"suggestions\": [\"bullet1\", \"bullet2\", ...]}."
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Resume: {resume_text[:2000]}\n\nJob Description: {job_description_text[:2000]}"}
        ],
        temperature=0.7,
        max_tokens=600
    )

    response_content = response.choices[0].message.content
    try:
        # Remove markdown code blocks if present
        if response_content.startswith("```json"):
            response_content = response_content.replace("```json", "").replace("```", "").strip()
        elif response_content.startswith("```"):
            response_content = response_content.replace("```", "").strip()

        # Extract JSON from the response (look for first { to last })
        start_idx = response_content.find('{')
        end_idx = response_content.rfind('}')
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_content = response_content[start_idx:end_idx+1]
            return json.loads(json_content)

        # Try to parse the entire content as JSON
        return json.loads(response_content)
    except json.JSONDecodeError:
        # If JSON parsing fails, return structured response
        return {
            "fit_percentage": 0,
            "reasons": ["Unable to parse structured response"],
            "suggestions": ["Please check the AI model response format"],
            "raw_response": response_content
        }