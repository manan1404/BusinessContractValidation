import os
import sys
import streamlit as st
import nltk
from nltk.corpus import stopwords

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from pdf_highlighting import highlight_differences

st.title("Business Contract Validation")

# Ensure NLTK stopwords are available
nltk_data_path = os.getenv('NLTK_DATA', '/usr/share/nltk_data')
if not os.path.exists(os.path.join(nltk_data_path, 'corpora/stopwords')):
    nltk.download('stopwords', download_dir=nltk_data_path)

# api_key = st.text_input("Enter your API Key", type="password")
api_key = "REMOVED"

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
