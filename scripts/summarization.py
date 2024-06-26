# scripts/summarization.py
from transformers import pipeline

# Load summarization model from HuggingFace transformers
summarizer = pipeline("summarization")

def summarize_text(text):
    """Summarize the provided text."""
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    return summary[0]['summary_text']
