import pytest
from src.data.loader import clean_text
from src.utils.nlp import tokenize


def test_clean_text():
    assert clean_text("Hello WORLD!!!") == "hello world"
    assert clean_text("Contact me at test@example.com") == "contact me at"
    assert clean_text("Call 555-123-4567") == "call"


def test_tokenize():
    # 'the', 'is' are usually stopwords
    tokens = tokenize("The quick brown fox jumps over the lazy dog.")
    assert "fox" in tokens
    assert "the" not in tokens
