# Use Python 3.11 explicitly
FROM python:3.11.9-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PORT=10000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    gcc \
    g++ \
    make \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python build tools with specific versions
RUN python -m pip install --upgrade pip==23.3.1
RUN pip install setuptools==68.2.2 wheel==0.41.2 Cython==0.29.36

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p backend/utils/output

# Download models (with error handling)
RUN python -c "import nltk; nltk.download('stopwords', quiet=True); nltk.download('punkt', quiet=True)" || true
RUN python -m spacy download en_core_web_sm || true

# Make scripts executable
RUN chmod +x start.sh

# Expose port
EXPOSE $PORT

# Start the application directly
CMD uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT --workers 1