# Use Python 3.11 for better compatibility
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # PDF processing dependencies
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    # Build dependencies
    gcc \
    g++ \
    make \
    # Network tools
    curl \
    wget \
    # Clean up
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set working directory
WORKDIR /app

# Upgrade pip and install build tools first
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies with specific flags for stability
RUN pip install --no-cache-dir \
    --timeout=1000 \
    --retries=5 \
    -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p backend/utils/output

# Download NLTK data
RUN python -c "import nltk; nltk.download('stopwords', quiet=True); nltk.download('punkt', quiet=True)"

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Set proper permissions
RUN chmod +x install_spacy_model.py start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:10000/health || exit 1

# Expose port
EXPOSE 10000

# Start command
CMD ["./start.sh"]