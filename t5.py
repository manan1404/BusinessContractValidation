import fitz
import nltk
import google.generativeai as genai
import time
import string
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

def remove_stopwords(word_list):
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in word_list if word.lower() not in stop_words]
    return filtered_words

# Configure the Gemini model
YOUR_API_KEY1 = "REMOVED"
genai.configure(api_key=YOUR_API_KEY1)
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 452048}
model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)

def formatter(text):
    translator = str.maketrans('', '', string.punctuation)
    text_no_punct = text.translate(translator)
    text_no_newlines = text_no_punct.replace('\n', ' ').replace('\r', '')
    return text_no_newlines

def extract_sentences(text):
    return nltk.sent_tokenize(text)

def get_different_sentences(sentences1, sentences2):
    differences = []

    generation_config = {
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 1,
                    "max_output_tokens": 12856,
                    "response_mime_type": "text/plain",
                }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config)
    
    chat_session = model.start_chat()
    prompt = f"Compare the following two sentences by analyzing the semantic meaning. You should identify any difference in meaning implied by sentence 1 when compared to sentence2.  Your response: if the sentences are different, answer should be 'YES' followed by the words in sentence1 that differ in sentence 2. Else if there's no difference answer is 'NO'. \nSentence 1: {sentences1}\nSentence 2: {sentences2}\n"
    response = chat_session.send_message(prompt)
    print("API CALL RESPONSE--------")
    ans = response.text
    print(ans)

    if "YES" in ans or 'yes' in ans:
        different_phrase = ans.split('YES')[1:]
        return different_phrase 
    return []

def highlight_sentence(page, sentence):
    words = page.get_text("words")
    sentence_words = sentence.split()
    sentence_words = remove_stopwords(sentence_words) #sk
    # # print(f'\n {words} \n')
    # print(f'\n SENTENCE {sentence_words} \n')
    for word in words:
        if word[4] in sentence_words:
            highlight = page.add_highlight_annot(fitz.Rect(word[:4]))
            highlight.update()


def highlight_differences(pdf_path1, pdf_path2, output_path):
    pdf1 = fitz.open(pdf_path1)
    pdf2 = fitz.open(pdf_path2)

    for page_num in range(len(pdf1)):
        page1 = pdf1.load_page(page_num)
        page2 = pdf2.load_page(page_num)

        text1 = page1.get_text()
        text2 = page2.get_text()

        text1 = formatter(text1)
        text2 = formatter(text2)

        differences = get_different_sentences(text1, text2)
        diff = remove_stopwords(differences)
        for w in diff:
            highlight_sentence(page1, w)
        time.sleep(2)

    pdf1.save(output_path)

# Paths to the PDF files
pdf_path1 = r"C:\Users\gauri\OneDrive\Desktop\BusinessContractValidation\BCV\Templates\intel_21.pdf"
pdf_path2 = r"C:\Users\gauri\OneDrive\Desktop\BusinessContractValidation\BCV\Templates\intel_22 .pdf"
output_path = r"C:\Users\gauri\OneDrive\Desktop\BusinessContractValidation\BCV\highlighted_diff.pdf"

# Highlight differences page by page
highlight_differences(pdf_path1, pdf_path2, output_path)
