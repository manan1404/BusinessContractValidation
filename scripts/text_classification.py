# scripts/text_classification.py
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def classify_text(texts, labels):
    # Vectorize the text data
    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(texts)

    # Define and train the classifier
    classifier = MultinomialNB()
    classifier.fit(X_train, labels)

    return classifier

    # Train a classifier
    #classifier = MultinomialNB()
    #classifier.fit(X_train, y_train)

    # Make predictions
    #y_pred = classifier.predict(X_test)

    # Evaluate the classifier
    #report = classification_report(y_test, y_pred)
    #return report