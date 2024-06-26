# app/test_import.py
import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(f"Adding {path} to sys.path")
sys.path.append(path)

try:
    from scripts.text_extraction import extract_text_from_pdf
    print("Import successful")
except ModuleNotFoundError as e:
    print(f"Import failed: {e}")
