"""
Simple TF-IDF implementation without scikit-learn dependency
"""
import re
import math
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class SimpleTFIDF:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        """Clean and tokenize text"""
        # Convert to lowercase and remove special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text.lower())

        # Tokenize
        tokens = word_tokenize(text)

        # Remove stopwords and short words
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]

        return tokens

    def compute_tf(self, tokens):
        """Compute term frequency"""
        tf_dict = {}
        total_tokens = len(tokens)

        for token in tokens:
            tf_dict[token] = tf_dict.get(token, 0) + 1

        # Normalize by total tokens
        for token in tf_dict:
            tf_dict[token] = tf_dict[token] / total_tokens

        return tf_dict

    def get_top_keywords(self, text, top_n=20):
        """Get top keywords from a single document"""
        tokens = self.preprocess_text(text)
        tf_scores = self.compute_tf(tokens)

        # Sort by frequency and return top N
        sorted_scores = sorted(tf_scores.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_scores[:top_n])

    def cosine_similarity(self, doc1_tfidf, doc2_tfidf):
        """Compute cosine similarity between two TF-IDF vectors"""
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
            return 0

        return dot_product / (magnitude1 * magnitude2)

    def compare_documents(self, doc1, doc2):
        """Compare two documents and return similarity metrics"""
        # Get TF scores for both documents
        tokens1 = self.preprocess_text(doc1)
        tokens2 = self.preprocess_text(doc2)

        tf1 = self.compute_tf(tokens1)
        tf2 = self.compute_tf(tokens2)

        # Calculate similarity
        similarity = self.cosine_similarity(tf1, tf2)

        # Find common keywords
        common_terms = set(tf1.keys()) & set(tf2.keys())
        common_keywords = []

        for term in common_terms:
            common_keywords.append({
                'term': term,
                'resume_score': tf1[term],
                'job_desc_score': tf2[term],
                'combined_importance': (tf1[term] + tf2[term]) / 2
            })

        # Sort by combined importance
        common_keywords.sort(key=lambda x: x['combined_importance'], reverse=True)

        return {
            'similarity_score': similarity,
            'common_keywords': common_keywords[:10],  # Top 10 common keywords
        }
