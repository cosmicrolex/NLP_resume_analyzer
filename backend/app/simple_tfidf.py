"""
Simple TF-IDF implementation without scikit-learn dependency
"""
import re
import math
import nltk
import spacy
from collections import Counter
from nltk.corpus import stopwords

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm", disable=["parser"])
    print("✅ spaCy model loaded successfully in SimpleTFIDF")
except OSError:
    print("⚠️ spaCy model not found in SimpleTFIDF, attempting to download...")
    try:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        nlp = spacy.load("en_core_web_sm", disable=["parser"])
        print("✅ spaCy model downloaded and loaded successfully in SimpleTFIDF")
    except Exception as e:
        print(f"❌ Failed to download spaCy model in SimpleTFIDF: {str(e)}")
        nlp = None
except Exception as e:
    print(f"❌ Failed to load spaCy model in SimpleTFIDF: {str(e)}")
    nlp = None

class SimpleTFIDF:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def extract_key_terms(self, text):
        """Extract domain-specific key terms (noun phrases) from text"""
        try:
            doc = nlp(text.lower())
            key_terms = set()
            for chunk in doc.noun_chunks:
                term = chunk.text.strip()
                # Limit to 1-3 words, exclude proper nouns, and cap character length
                if 1 <= len(term.split()) <= 3 and all(token.ent_type_ not in ['PERSON', 'ORG', 'GPE'] for token in chunk) and len(term.replace(' ', '')) <= 30:
                    key_terms.add(term)
            print(f"DEBUG - Extracted key terms: {list(key_terms)[:10]}...")
            return key_terms
        except Exception as e:
            print(f"DEBUG - Key term extraction failed: {str(e)}")
            return set()

    def assign_idf_score(self, term):
        """Assign heuristic IDF score based on term characteristics"""
        try:
            if len(term.split()) > 1:
                return 2.0  # Noun phrases
            elif nlp(term)[0].pos_ in ['NOUN', 'PROPN']:
                return 1.5  # Single nouns
            return 0.5  # Other terms
        except Exception:
            return 0.5  # Fallback for safety

    def preprocess_text(self, text):
        """Clean and tokenize text with dynamic key term handling"""
        if not text or not isinstance(text, str):
            print("DEBUG - Input text is empty or invalid")
            return []
        
        # Convert to lowercase and remove special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text.lower())

        # Extract key terms
        key_terms = self.extract_key_terms(text)
        
        # Tokenize with spaCy
        try:
            doc = nlp(text)
        except Exception as e:
            print(f"DEBUG - spaCy tokenization failed: {str(e)}")
            return []
        
        # Preserve key terms
        tokens = []
        i = 0
        while i < len(doc):
            found_term = False
            for term in key_terms:
                term_words = term.split()
                term_length = len(term_words)
                if i + term_length <= len(doc):
                    if ' '.join([doc[i + j].text for j in range(term_length)]) == term:
                        tokens.append(term)
                        i += term_length
                        found_term = True
                        break
            if not found_term:
                token = doc[i]
                if token.ent_type_ not in ['PERSON', 'ORG', 'GPE'] and len(token.text) > 2 and token.text not in self.stop_words:
                    tokens.append(token.text)
                i += 1
        
        print(f"DEBUG - Preprocessed tokens: {tokens[:20]}...")
        return tokens

    def compute_tf(self, tokens):
        """Compute term frequency with boost for key terms"""
        tf_dict = {}
        total_tokens = len(tokens) if tokens else 1  # Avoid division by zero
        
        # Extract key terms from tokens
        key_terms = set([token for token in tokens if len(token.split()) > 1])
        
        # Compute term frequency
        for token in tokens:
            tf_dict[token] = tf_dict.get(token, 0) + 1
        
        # Apply boost to key terms
        for term in key_terms:
            if term in tf_dict:
                tf_dict[term] *= 2  # Boost factor
        
        # Normalize by total tokens
        for token in tf_dict:
            tf_dict[token] = tf_dict[token] / total_tokens
        
        return tf_dict

    def compute_tf_idf(self, tokens):
        """Compute TF-IDF with heuristic IDF scores"""
        tf_dict = self.compute_tf(tokens)
        tfidf_dict = {}
        
        for token in tf_dict:
            idf = self.assign_idf_score(token)
            tfidf_dict[token] = tf_dict[token] * idf
        
        return tfidf_dict

    def get_top_keywords(self, text, top_n=20):
        """Get top keywords with TF-IDF"""
        tokens = self.preprocess_text(text)
        if not tokens:
            print("DEBUG - No tokens after preprocessing")
            return {}
        
        tfidf_scores = self.compute_tf_idf(tokens)
        
        # Filter out long concatenated terms
        tfidf_scores = {k: v for k, v in tfidf_scores.items() if len(k.replace(' ', '')) <= 30}
        
        # Sort by TF-IDF score and return top N
        sorted_scores = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_scores[:top_n])

    def cosine_similarity(self, doc1_tfidf, doc2_tfidf):
        """Compute cosine similarity between two TF-IDF vectors"""
        if not doc1_tfidf or not doc2_tfidf:
            print("DEBUG - One or both TF-IDF dictionaries are empty")
            return 0.0

        # Get all unique terms
        all_terms = set(doc1_tfidf.keys()) | set(doc2_tfidf.keys())

        # Create vectors
        vec1 = [doc1_tfidf.get(term, 0) for term in all_terms]
        vec2 = [doc2_tfidf.get(term, 0) for term in all_terms]

        # Compute dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))

        # Compute magnitudes
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))

        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            print("DEBUG - Zero magnitude in cosine similarity")
            return 0.0

        return dot_product / (magnitude1 * magnitude2)

    def compare_documents(self, doc1, doc2):
        """Compare two documents and return similarity metrics"""
        # Get TF-IDF scores for both documents
        tokens1 = self.preprocess_text(doc1)
        tokens2 = self.preprocess_text(doc2)

        tfidf1 = self.compute_tf_idf(tokens1)
        tfidf2 = self.compute_tf_idf(tokens2)

        # Calculate similarity
        similarity = self.cosine_similarity(tfidf1, tfidf2)

        # Find common keywords
        common_terms = set(tfidf1.keys()) & set(tfidf2.keys())
        common_keywords = []

        for term in common_terms:
            common_keywords.append({
                'term': term,
                'resume_score': tfidf1[term],
                'job_desc_score': tfidf2[term],
                'combined_importance': (tfidf1[term] + tfidf2[term]) / 2
            })

        # Sort by combined importance
        common_keywords.sort(key=lambda x: x['combined_importance'], reverse=True)

        return {
            'similarity_score': similarity,
            'common_keywords': common_keywords[:10],  # Top 10 common keywords
        }