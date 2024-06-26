# tests/test_ocr.py
from scripts.ocr import ocr_image

def test_ocr_image():
    result = ocr_image("data/sample_contracts/sample_image.png")
    assert "expected text" in result
