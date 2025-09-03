# backend/jd_analyzer.py
from sklearn.feature_extraction.text import TfidfVectorizer
from .tfidf_analyzer import preprocess_text  # Reuse preprocess_text from tfidf_analyzer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

nltk.download('punkt')

def analyze_jd_with_tfidf(jd_text):
    """
    Analyze a job description text using TF-IDF and return top keywords with scores.
    
    Args:
        jd_text (str): The job description text to analyze.
        
    Returns:
        dict: A dictionary with top_keywords list, each containing term and TF-IDF score.
    """
    try:
        # Preprocess the JD text (reuse preprocess_text from tfidf_analyzer)
        processed_text = preprocess_text(jd_text)
        if not processed_text:
            print("Warning: Processed text is empty after preprocessing")
            return {"top_keywords": []}

        # Initialize TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            max_features=10,  # Limit to top 10 keywords
            stop_words=stopwords.words('english'),
            ngram_range=(1, 2)  # Include unigrams and bigrams
        )

        # Compute TF-IDF matrix
        tfidf_matrix = vectorizer.fit_transform([processed_text])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]

        # Get top keywords with scores
        top_keywords = [
            {"term": feature_names[i], "score": round(float(scores[i]), 4)}
            for i in scores.argsort()[-10:][::-1] if scores[i] > 0
        ]

        return {"top_keywords": top_keywords}
    
    except Exception as e:
        print(f"Error in JD TF-IDF analysis: {str(e)}")
        return {"top_keywords": [], "error": str(e)}