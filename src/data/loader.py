from pathlib import Path


def load_custom_stopwords():
    """
    Load custom stopwords from file

    Returns:
        set: Set of custom stopwords
    """
    stopwords_file = Path(__file__).parent / "stopwords.txt"

    custom_stopwords = set()

    try:
        with open(stopwords_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    custom_stopwords.add(line.lower())
    except FileNotFoundError:
        print("Warning: stopwords.txt not found")

    return custom_stopwords
