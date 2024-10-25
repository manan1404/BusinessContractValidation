# app/streamlit_app.py
import os
import sys
import streamlit as st
import nltk
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from pdf_highlighting import highlight_differences
load_dotenv()

st.title("Business Contract Validation")

# Download NLTK stopwords if not already present
nltk.download('stopwords')

# api_key = st.text_input("Enter your API Key", type="password")
api_key = os.getenv("API_KEY")

pdf1 = st.file_uploader("Upload the first PDF", type="pdf")
pdf2 = st.file_uploader("Upload the second PDF", type="pdf")

if pdf1 and pdf2 and api_key:
    os.makedirs("data/samples", exist_ok=True)

    with open("data/samples/temp1.pdf", "wb") as f:
        f.write(pdf1.getbuffer())

    with open("data/samples/temp2.pdf", "wb") as f:
        f.write(pdf2.getbuffer())

    output_path = "data/samples/highlighted_diff.pdf"

    if st.button("Generate Differences PDF"):
        highlight_differences("data/samples/temp1.pdf", "data/samples/temp2.pdf", output_path, api_key)
        st.success("Differences highlighted successfully!")
        with open(output_path, "rb") as f:
            st.download_button("Download Highlighted PDF", f, file_name="highlighted_diff.pdf")
