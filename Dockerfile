FROM python:3.12-slim

# Install poppler-utils for pdf2image
RUN apt-get update && apt-get install -y poppler-utils \ tesseract-ocr \ libtesseract-dev \ && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 10000
CMD ["python", "start_app.py"]