import re
import nltk  # type: ignore
from nltk.corpus import stopwords  # type: ignore
from nltk.tokenize import word_tokenize  # type: ignore
from nltk.stem import WordNetLemmatizer  # type: ignore

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")


def clean_text(text):
    """
    clean and normalize text

    Args:
        text (str): Raw input text

    Returns:
        str: Cleaned text
    """
    # convert to lowercase
    text = text.lower()

    # remove special characters and extra whitespaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_keywords(text, max_keywords=20, min_length=3):
    """
    Extract important keywords from text

    Args:
        text (str): input text
        max_keywords (int): Maximum number of keywords to return
        min_length (int): Minimum keyword length

    Returns:
        list: List of keywords strings
    """
    from src.data.loader import load_custom_stopwords  # type: ignore

    # Initialize lemmatizer
    lemmatizer = WordNetLemmatizer()

    # clean text
    cleaned = clean_text(text)

    # Tokenize
    tokens = word_tokenize(cleaned)

    # load stopwrds (NLTK + custom)
    nltk_stopwords = set(stopwords.words("english"))
    custom_stopwords = load_custom_stopwords()
    all_stopwords = nltk_stopwords.union(custom_stopwords)

    keywords = []
    for word in tokens:
        # lemmatize the word
        lemmatized = lemmatizer.lemmatize(word)

        # Keep if not a stopword and meets length requirement
        if lemmatized not in all_stopwords and len(lemmatized) >= min_length:
            keywords.append(lemmatized)

    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for word in keywords:
        if word not in seen:
            seen.add(word)
            unique_keywords.append(word)

    return unique_keywords[:max_keywords]


if __name__ == "__main__":
    print("=== Testing Improved Keyword Extraction ===\n")

    # Test 1: Simple text
    sample1 = "Python developer with 5+ years experience in Machine Learning!"
    print("Test 1 - Simple:")
    print("Original:", sample1)
    print("Keywords:", extract_keywords(sample1))
    print()

    # Test 2: Real job description
    sample2 = """
    We are looking for a Senior Python Developer with strong experience in 
    backend development. Must have knowledge of REST APIs, microservices, 
    Docker, and Kubernetes. Experience with AWS cloud services is a plus.
    The ideal candidate will be responsible for designing and building 
    scalable distributed systems.
    """
    print("Test 2 - Real Job Description:")
    print("Keywords:", extract_keywords(sample2, max_keywords=15))
    print()

    # Test 3: Check lemmatization
    sample3 = (
        "Building scalable services using Docker containers and Kubernetes pipelines"
    )
    print("Test 3 - Lemmatization Check:")
    print("Original:", sample3)
    print("Keywords:", extract_keywords(sample3))
    print("\n=== Test Complete ===")
