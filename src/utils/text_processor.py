import re
import nltk  # type: ignore
from nltk.corpus import stopwords # type: ignore
from nltk.tokenize import word_tokenize # type: ignore


try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")


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
    # clean text
    cleaned = clean_text(text)

    # Tokenize
    tokens = word_tokenize(cleaned)

    # remove stopwords and short words
    stop_words = set(stopwords.words("english"))
    keywords = [
        word for word in tokens if word not in stop_words and len(word) >= min_length
    ]

    seen = set()
    unique_keywords = []
    for word in keywords:
        if word not in seen:
            seen.add(word)
            unique_keywords.append(word)

    return unique_keywords[:max_keywords]


# test

if __name__ == "__main__":
    print("=== Testing text_processor ===")
    sample = "Python developer with 5+ years expericne in Machine Learning!"
    print("Original:", sample)
    print("Cleaned:", clean_text(sample))
    print("Keywords:", extract_keywords(sample))
    print("=== Test complete ===")
