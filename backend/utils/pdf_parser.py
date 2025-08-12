
import pdfplumber
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import pathlib
import re
from bs4 import BeautifulSoup

def extract_with_pdfplumber(file_path):
    """
    Extract text from PDF using pdfplumber.
    """
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

def extract_with_ocr(file_path):
    """
    Extract text from PDF using OCR if pdfplumber fails.
    """
    images = convert_from_path(file_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def clean_extracted_text(text):
    """
    Clean extracted text by removing HTML tags, bullet points, extra whitespace, and newlines.
    
    Args:
        text (str): Raw extracted text
    
    Returns:
        str: Cleaned text
    """
    # Remove HTML tags if any
    text = BeautifulSoup(text, "html.parser").get_text()
    
    # Remove bullet points and special characters
    text = re.sub(r'[•➢]', '', text)  # Remove common bullet points
    text = re.sub(r'[^\w\s.,-]', '', text)  # Keep alphanumeric, spaces, and basic punctuation
    text = re.sub(r'\n+', ' ', text)  # Replace newlines with spaces
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    text = re.sub(r'\bxx\b', '', text)     # Remove standalone 'xx'
    text = re.sub(r'\b\d{2}xx\b', '', text)  # Remove year placeholders like 20xx, 19xx

    
    return text

def extract_text_from_any_pdf(file_path):
    """
    Extract and clean text from any PDF, using pdfplumber or OCR as fallback.
    
    Args:
        file_path (str): Path to the PDF file
    
    Returns:
        str: Cleaned extracted text
    """
    text = extract_with_pdfplumber(file_path)
    if not text.strip():
        print("No text found with pdfplumber. Switching to OCR...")
        text = extract_with_ocr(file_path)
    return clean_extracted_text(text)

def save_text_to_file(text, output_path):
    """
    Save cleaned text to a file.
    
    Args:
        text (str): Text to save
        output_path (str): Path to save the text file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"✅ Text successfully saved to {output_path}")
    except Exception as e:
        print(f"⚠️ Error saving file: {e}")

def textextractionfunction(file_path, output_path):
    """
    Main function to extract and save cleaned text from a PDF.
    
    Args:
        file_path (str): Path to the input PDF
        output_path (str): Path to save the output text file
    
    Returns:
        str: Cleaned extracted text
    """
    text = extract_text_from_any_pdf(file_path)
    save_text_to_file(text, output_path)
    return text

if __name__ == "__main__":
    outpath = pathlib.Path(__file__).resolve().parent
    filepath = outpath / "sample.pdf"  # Adjust as needed
    outputpath = outpath / "output.txt"
    textextractionfunction(filepath, outputpath)
