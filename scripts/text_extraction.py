import pdfplumber

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


def preprocess_text(texts):
    """Preprocess text eg -> converting to lowercase)."""
    return [text.lower() for text in texts]

