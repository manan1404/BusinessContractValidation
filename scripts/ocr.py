# scripts/ocr.py
import pytesseract
from PIL import Image

def ocr_image(image_path):
    """Extract text from an image file using OCR."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text
