FROM python:3.12-slim

# Install system dependencies for pdf2image (poppler-utils) and pytesseract (tesseract-ocr)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Download spaCy model after copying code
RUN python install_spacy_model.py

# Expose port (Render uses 10000 by default)
EXPOSE 10000

# Start FastAPI with uvicorn
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "10000"]