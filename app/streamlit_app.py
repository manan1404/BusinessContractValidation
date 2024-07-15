import os
import sys
import streamlit as st
import nltk
from nltk.corpus import stopwords
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from pdf_highlighting import highlight_differences

# Download NLTK stopwords if not already present
nltk.download('stopwords')

# Get the API key from Streamlit secrets
api_key = st.secrets["API_KEY"]

st.title("Business Contract Validation")

if not api_key:
    st.error("API Key not found. Please set the API_KEY in Streamlit secrets.")
else:
    pdf1 = st.file_uploader("Upload the first PDF", type="pdf")
    pdf2 = st.file_uploader("Upload the second PDF", type="pdf")

    if pdf1 and pdf2:
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