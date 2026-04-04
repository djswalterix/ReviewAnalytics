"""
Shared text preprocessing for training and inference.

Both train.py and api.py import from here to guarantee that the same
transformations are applied at training time and at inference time.
"""
import string
import subprocess

try:
    import spacy
except ImportError:
    subprocess.run(['pip', 'install', 'spacy'], check=True)
    import spacy

SPACY_MODEL = 'it_core_news_sm'

try:
    _nlp = spacy.load(SPACY_MODEL)
except OSError:
    print(f"⚠️  spaCy model '{SPACY_MODEL}' not found. Installing...")
    subprocess.run(['python', '-m', 'spacy', 'download', SPACY_MODEL], check=True)
    _nlp = spacy.load(SPACY_MODEL)


def preprocess_and_lemmatize(text: str) -> str:
    """Remove punctuation and lemmatize Italian text.

    Examples:
        "pulita"  → "pulito"
        "camere." → "camera"
    """
    text = text.translate(str.maketrans('', '', string.punctuation))
    doc = _nlp(text)
    return ' '.join(token.lemma_ for token in doc)
