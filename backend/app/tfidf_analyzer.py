import re
import json
import nltk
import spacy
from nltk.corpus import stopwords
import os
from openai import OpenAI
from dotenv import load_dotenv
from simple_tfidf import SimpleTFIDF

# Load environment variables from root directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# Note: GROQ client is initialized dynamically with user-provided API keys
# No static client initialization needed since we use dynamic API keys
client = None  # Placeholder for dynamic client initialization
print("✅ GROQ client will be initialized dynamically with user-provided API keys")

# Download NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# Load spaCy model for NER and noun chunking
try:
    nlp = spacy.load("en_core_web_sm", disable=["parser"])
    print("✅ spaCy model loaded successfully")
except OSError:
    print("⚠️ spaCy model not found, attempting to download...")
    try:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        nlp = spacy.load("en_core_web_sm", disable=["parser"])
        print("✅ spaCy model downloaded and loaded successfully")
    except Exception as e:
        print(f"❌ Failed to download spaCy model: {str(e)}")
        nlp = None
except Exception as e:
    print(f"❌ Failed to load spaCy model: {str(e)}")
    nlp = None

def preprocess_text(text):
    """Enhanced preprocessing to extract domain-specific terms and remove irrelevant entities"""
    if not text or not isinstance(text, str):
        print("DEBUG - Input text is empty or invalid")
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove special characters but keep letters, numbers, spaces, and hyphens
    text = re.sub(r'[^a-zA-Z0-9\s\-]', ' ', text)
    
    # Remove standalone years (2020, 2021, etc.)
    text = re.sub(r'\b(19|20)\d{2}\b', '', text)
    
    # If spaCy is not available, use basic preprocessing
    if nlp is None:
        print("DEBUG - spaCy not available, using basic preprocessing")
        # Basic tokenization and stopword removal
        words = text.split()
        minimal_stopwords = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'between', 'among', 'this', 'that', 'these', 'those', 'is', 'was', 'are',
            'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall'
        }
        filtered_words = [word for word in words if word not in minimal_stopwords and len(word) > 2]
        return ' '.join(filtered_words)
    
    # Tokenize with spaCy
    try:
        doc = nlp(text)
    except Exception as e:
        print(f"DEBUG - spaCy tokenization failed: {str(e)}")
        # Fallback to basic preprocessing
        words = text.split()
        minimal_stopwords = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'between', 'among', 'this', 'that', 'these', 'those', 'is', 'was', 'are',
            'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall'
        }
        filtered_words = [word for word in words if word not in minimal_stopwords and len(word) > 2]
        return ' '.join(filtered_words)
    
    # Extract noun phrases (1-3 words) as key terms
    key_terms = set()
    for chunk in doc.noun_chunks:
        term = chunk.text.lower().strip()
        # Limit to 1-3 words, exclude proper nouns
        if 1 <= len(term.split()) <= 3 and all(token.ent_type_ not in ['PERSON', 'ORG', 'GPE'] for token in chunk):
            # Exclude terms longer than 30 characters to prevent sentence-like phrases
            if len(term.replace(' ', '')) <= 30:
                key_terms.add(term)
    
    # Log rejected terms for debugging
    rejected_terms = [chunk.text.lower().strip() for chunk in doc.noun_chunks if chunk.text.lower().strip() not in key_terms]
    print(f"DEBUG - Rejected terms: {rejected_terms[:10]}...")
    
    # Tokenize while preserving key terms
    filtered_tokens = []
    i = 0
    while i < len(doc):
        found_term = False
        for term in key_terms:
            term_words = term.split()
            term_length = len(term_words)
            if i + term_length <= len(doc):
                if ' '.join([doc[i + j].text for j in range(term_length)]) == term:
                    filtered_tokens.append(term)
                    i += term_length
                    found_term = True
                    break
        if not found_term:
            token = doc[i]
            if token.ent_type_ not in ['PERSON', 'ORG', 'GPE'] and 2 <= len(token.text) <= 20:
                filtered_tokens.append(token.text)
            i += 1
    
    # Minimal stopword removal
    minimal_stopwords = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
        'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above',
        'below', 'between', 'among', 'this', 'that', 'these', 'those', 'is', 'was', 'are',
        'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall'
    }
    
    # Filter stopwords but keep key terms
    filtered_words = [word for word in filtered_tokens if word not in minimal_stopwords or word in key_terms]
    
    result = ' '.join(filtered_words)
    print(f"DEBUG - Preprocessed text preview: {result[:200]}...")
    print(f"DEBUG - Extracted key terms: {list(key_terms)[:10]}...")
    return result

def analyze_resume_with_tfidf(resume_text):
    try:
        print(f"DEBUG - Original resume text length: {len(resume_text)}")

        # Initialize our custom TF-IDF analyzer
        tfidf_analyzer = SimpleTFIDF()

        # Get top keywords using our custom implementation
        keyword_scores = tfidf_analyzer.get_top_keywords(resume_text, top_n=20)

        # Filter keywords to exclude irrelevant terms
        filtered_keywords = {
            term: score for term, score in keyword_scores.items()
            if term not in ['name', 'university', 'college', 'institute', 'department']
            and len(term.replace(' ', '')) <= 30  # Prevent long concatenated terms
        }

        print(f"DEBUG - Resume features found: {len(filtered_keywords)}")
        print(f"DEBUG - Top resume features: {list(filtered_keywords.keys())[:10]}")

        # Prepare top keywords for display
        top_keywords = []
        for term, score in filtered_keywords.items():
            top_keywords.append({
                "term": term,
                "score": round(float(score), 4)  # Ensure score is float
            })

        # Sort by score for consistency
        top_keywords = sorted(top_keywords, key=lambda x: x["score"], reverse=True)

        # LLM analysis for strengths and weaknesses
        llm_analysis = None
        if client and os.getenv("GROQ_API_KEY"):
            try:
                llm_analysis = get_resume_strengths_weaknesses(resume_text, filtered_keywords)
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
        return {
            "top_keywords": [],  # Return empty list to avoid frontend error
            "llm_strengths_weaknesses": {"error": f"TF-IDF analysis failed: {str(e)}"}
        }

def get_resume_strengths_weaknesses(resume_text, tfidf_scores):
    """Use Groq LLM to identify resume strengths and weaknesses."""
    top_terms = ", ".join([f"{term}: {score:.4f}" for term, score in sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:10]])
    system_prompt = (
        "You are a career advisor specializing in professional roles. Analyze the provided resume text, focusing on domain-specific skills, tools, and experiences relevant to the job domain (e.g., technical skills for tech roles, financial skills for finance roles). "
        f"Ignore proper nouns (e.g., names, universities, companies) unless directly relevant to expertise. Use the top TF-IDF keywords for context: {top_terms}. "
        "Identify 3-5 key strengths (e.g., specific skills, projects, achievements) and 3-5 weaknesses (e.g., missing skills, lack of experience). "
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

        # Extract JSON from the response
        start_idx = response_content.find('{')
        end_idx = response_content.rfind('}')
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_content = response_content[start_idx:end_idx+1]
            return json.loads(json_content)

        return json.loads(response_content)
    except json.JSONDecodeError:
        return {
            "strengths": ["Unable to parse structured response"],
            "weaknesses": ["Please check the AI model response format"],
            "raw_response": response_content
        }

def analyze_job_description_with_tfidf(job_description_text):
    try:
        print(f"DEBUG - Original job desc text length: {len(job_description_text)}")

        # Initialize our custom TF-IDF analyzer
        tfidf_analyzer = SimpleTFIDF()

        # Get top keywords using our custom implementation
        keyword_scores = tfidf_analyzer.get_top_keywords(job_description_text, top_n=20)

        # Filter keywords to exclude irrelevant terms
        filtered_keywords = {
            term: score for term, score in keyword_scores.items()
            if term not in ['name', 'university', 'college', 'institute', 'department']
            and len(term.replace(' ', '')) <= 30  # Prevent long concatenated terms
        }

        print(f"DEBUG - Job desc features found: {len(filtered_keywords)}")
        print(f"DEBUG - Top job desc features: {list(filtered_keywords.keys())[:10]}")

        # Prepare top keywords for display
        top_keywords = []
        for term, score in filtered_keywords.items():
            top_keywords.append({
                "term": term,
                "score": round(float(score), 4)  # Ensure score is float
            })

        # Sort by score for consistency
        top_keywords = sorted(top_keywords, key=lambda x: x["score"], reverse=True)

        return {
            "top_keywords": top_keywords
        }
    except Exception as e:
        print(f"DEBUG - Job desc analysis error: {str(e)}")
        return {
            "top_keywords": [],  # Return empty list to avoid frontend error
            "error": f"TF-IDF analysis failed: {str(e)}"
        }

def calculate_resume_job_similarity(resume_text, job_description_text):
    try:
        print("DEBUG - Starting similarity calculation...")

        if not resume_text.strip() or not job_description_text.strip():
            print("DEBUG - One or both texts are empty")
            return {
                "similarity_score": 0.0,
                "match_quality": "Poor Match",
                "common_keywords": [],
                "total_features": 0
            }

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
            "similarity_score": round(float(similarity_score), 4),
            "match_quality": match_quality,
            "common_keywords": common_terms,
            "total_features": len(common_terms)
        }
        
    except Exception as e:
        print(f"DEBUG - Similarity calculation error: {str(e)}")
        return {
            "similarity_score": 0.0,
            "match_quality": "Poor Match",
            "common_keywords": [],
            "total_features": 0,
            "error": f"Similarity calculation failed: {str(e)}"
        }

def comprehensive_resume_job_analysis(resume_text, job_description_text):
    try:
        print("DEBUG - Starting comprehensive analysis...")
        resume_analysis = analyze_resume_with_tfidf(resume_text)
        job_desc_analysis = analyze_job_description_with_tfidf(job_description_text)
        similarity_analysis = calculate_resume_job_similarity(resume_text, job_description_text)
        
        # LLM analysis for job fit
        llm_fit = None
        if client and os.getenv("GROQ_API_KEY"):
            try:
                llm_fit = get_resume_job_fit(resume_text, job_description_text, similarity_analysis)
                print(f"DEBUG - LLM fit assessment result: {llm_fit}")
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
        return {
            "resume_analysis": {"top_keywords": [], "error": f"Analysis failed: {str(e)}"},
            "job_description_analysis": {"top_keywords": [], "error": f"Analysis failed: {str(e)}"},
            "similarity_analysis": {
                "similarity_score": 0.0,
                "match_quality": "Poor Match",
                "common_keywords": [],
                "total_features": 0
            },
            "llm_fit_assessment": {"error": f"Comprehensive analysis failed: {str(e)}"}
        }

def get_resume_job_fit(resume_text, job_description_text, similarity_analysis):
    """Use Groq LLM to assess resume fit for the job description."""
    sim_score = similarity_analysis.get("similarity_score", 0)
    common_terms_str = ", ".join([f"{kw['term']}: {kw['combined_importance']:.4f}" for kw in similarity_analysis.get("common_keywords", [])[:5]])
    system_prompt = (
        f"You are a hiring manager for a professional role. Assess how well the provided resume fits the job description, focusing on domain-specific skills, tools, and experiences (e.g., technical skills for tech roles, financial skills for finance roles). "
        f"Ignore proper nouns (e.g., names, universities, companies) unless directly relevant to expertise. Consider the cosine similarity score ({sim_score}) and top common keywords ({common_terms_str}). "
        "Provide: 1. Estimated fit percentage (0-100%). 2. 3-5 reasons why the resume fits well (emphasizing relevant skills). "
        "3. 3-5 suggestions for improving the resume to better match the job (focusing on relevant skills). Return the response in JSON format: "
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

        # Extract JSON from the response
        start_idx = response_content.find('{')
        end_idx = response_content.rfind('}')
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_content = response_content[start_idx:end_idx+1]
            return json.loads(json_content)

        return json.loads(response_content)
    except json.JSONDecodeError:
        return {
            "fit_percentage": 0,
            "reasons": ["Unable to parse structured response"],
            "suggestions": ["Please check the AI model response format"],
            "raw_response": response_content
        }