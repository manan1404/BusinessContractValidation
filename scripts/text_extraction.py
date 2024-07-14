#scripts/text_extraction.py

import string
from nltk.corpus import stopwords

def remove_stopwords(word_list):
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in word_list if word.lower() not in stop_words]
    return filtered_words

def formatter(text):
    translator = str.maketrans('', '', string.punctuation)
    text_no_punct = text.translate(translator)
    text_no_newlines = text_no_punct.replace('\n', ' ').replace('\r', '')
    return text_no_newlines