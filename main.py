# main.py
from datasets import load_dataset
from scripts.text_extraction import preprocess_text
from scripts.ner import ner
from scripts.text_classification import classify_text
from scripts.text_comparison import compare_texts
from scripts.pdf_highlighting import highlight_pdf
from scripts.summarization import summarize_text


def main():
    data = load_dataset("lex_glue", "case_hold")
    train_data = data['train']

    # context and labels extract (revisit this - error)
    texts = train_data['context']
    labels = train_data['label']

    # text preproc(revisit - error)
    texts = preprocess_text(texts)

    # NER proc(not working)
    entities = [ner(text) for text in texts]
    print("Entities:", entities)

    classified_texts = classify_text(texts, labels)
    print("Classification Report:", classified_texts)

    text1 = "sample contract text."
    text2 = "sample reviewed contract text."
    differences = compare_texts(text1, text2)
    print("Differences:", differences)

    summary = summarize_text(" ".join(differences))
    print("Summary:", summary)

    # PDF highlighting (check)
    input_pdf = '.pdf'
    output_pdf = '.pdf'
    highlights = {0: [(100, 100, 200, 20)]}
    highlight_pdf(input_pdf, output_pdf, highlights)

if __name__ == "__main__":
    main()
