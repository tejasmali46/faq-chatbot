import json
import nltk
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
import nltk

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

# Load FAQ data
with open("faq.json", "r") as file:
    faq_data = json.load(file)

questions = [item["question"] for item in faq_data]
answers = [item["answer"] for item in faq_data]


def preprocess(text):
    text = text.lower()

    # Remove punctuation
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    tokens = word_tokenize(text)

    stop_words = set(stopwords.words("english"))

    words = [
        word for word in tokens
        if word not in stop_words
    ]

    return " ".join(words)

processed_questions = [preprocess(q) for q in questions]

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    sublinear_tf=True
)


question_vectors = vectorizer.fit_transform(processed_questions)


def get_answer(user_question):

    # Handle greetings
    question = user_question.lower().strip()

    if question in ["hi", "hello", "hey"]:
        return "Hello! 👋 How can I help you today?"

    if question in ["thanks", "thank you", "thx"]:
        return "You're welcome! 😊"

    if question in ["bye", "goodbye", "see you"]:
        return "Goodbye! Have a great day! 👋"

    # NLP Processing
    processed_question = preprocess(user_question)

    user_vector = vectorizer.transform([processed_question])

    similarity = cosine_similarity(user_vector, question_vectors)

    best_match = similarity.argmax()

    score = similarity[0][best_match]

    if score < 0.2:
        return "Sorry, I couldn't find a relevant answer. Please try asking differently."

    return answers[best_match]