import string
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = ''.join([c for c in text if c not in string.punctuation])
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return ' '.join(words)

def predict_review(review, model, vectorizer):
    clean = clean_text(review)
    vec = vectorizer.transform([clean])
    pred = model.predict(vec)[0]
    return "Fake ❌" if pred == 1 else "Genuine ✅"
