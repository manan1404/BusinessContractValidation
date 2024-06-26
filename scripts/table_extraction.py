# scripts/table_extraction.py
import tabula

def extract_tables_from_pdf(pdf_path):
    tables = tabula.read_pdf(pdf_path, pages='all')  # extract table from pdf
    return tables
