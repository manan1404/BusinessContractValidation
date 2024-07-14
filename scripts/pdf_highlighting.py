#scripts/pdf_highlighting.py

import fitz
import nltk
import google.generativeai as genai
import time
import string
from nltk.corpus import stopwords
from text_extraction import remove_stopwords, formatter  # Use absolute import


def extract_sentences(text):
    return nltk.sent_tokenize(text)


def get_different_sentences(sentences1, sentences2, api_key):
    differences = []

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 1,
        "max_output_tokens": 12856,
        "response_mime_type": "text/plain",
    }

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)

    chat_session = model.start_chat()
    prompt = f"Compare the following two sentences by analyzing the semantic meaning. You should identify any difference in meaning implied by sentence 1 when compared to sentence 2. Your response: if the sentences are different, answer should be 'YES' followed by the words in sentence 1 that differ in sentence 2. Else if there's no difference answer is 'NO'. \nSentence 1: {sentences1}\nSentence 2: {sentences2}\n"
    response = chat_session.send_message(prompt)
    ans = response.text

    if "YES" in ans or 'yes' in ans:
        different_phrase = ans.split('YES')[1:]
        return different_phrase
    return []


def highlight_sentence(page, sentence):
    words = page.get_text("words")
    sentence_words = sentence.split()
    sentence_words = remove_stopwords(sentence_words)

    for word in words:
        if word[4] in sentence_words:
            highlight = page.add_highlight_annot(fitz.Rect(word[:4]))
            highlight.update()


def highlight_differences(pdf_path1, pdf_path2, output_path, api_key):
    pdf1 = fitz.open(pdf_path1)
    pdf2 = fitz.open(pdf_path2)

    for page_num in range(len(pdf1)):
        page1 = pdf1.load_page(page_num)
        page2 = pdf2.load_page(page_num)

        text1 = page1.get_text()
        text2 = page2.get_text()

        text1 = formatter(text1)
        text2 = formatter(text2)

        differences = get_different_sentences(text1, text2, api_key)
        diff = remove_stopwords(differences)
        for w in diff:
            highlight_sentence(page1, w)
        time.sleep(2)

    pdf1.save(output_path)