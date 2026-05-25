import pandas as pd

from src.data.loader import clean_text, load_labeled_tickets
from src.utils.nlp import tokenize


def test_clean_text():
    assert clean_text("Hello WORLD!!!") == "hello world"
    assert clean_text("Contact me at test@example.com") == "contact me at"
    assert clean_text("Call 555-123-4567") == "call"


def test_clean_text_edge_cases():
    import numpy as np

    assert clean_text(None) == ""
    assert clean_text(np.nan) == ""
    assert clean_text("   Lots   of   spaces   ") == "lots of spaces"
    assert clean_text("Remove {product_purchased} token") == "remove token"


def test_tokenize():
    # 'the', 'is' are usually stopwords
    tokens = tokenize("The quick brown fox jumps over the lazy dog.")
    assert "fox" in tokens
    assert "the" not in tokens


def test_load_labeled_tickets_simple_schema(tmp_path):
    fp = tmp_path / "simple.csv"
    pd.DataFrame({"text": ["refund please", "app crashed"], "category": ["Billing", "Bug"]}).to_csv(fp, index=False)
    texts, labels = load_labeled_tickets(fp)
    assert texts == ["refund please", "app crashed"]
    assert labels == ["Billing", "Bug"]


def test_load_labeled_tickets_detects_columns_and_cleans(tmp_path):
    # Kaggle/Bitext-style schema: columns auto-detected, subject+body combined & cleaned.
    fp = tmp_path / "real.csv"
    pd.DataFrame(
        {
            "Ticket Subject": ["Refund REQUEST!"],
            "Ticket Description": ["Email me at a@b.com about the charge"],
            "Ticket Type": ["Billing inquiry"],
        }
    ).to_csv(fp, index=False)
    texts, labels = load_labeled_tickets(fp)
    assert labels == ["Billing inquiry"]
    # lowercased, punctuation + email stripped, subject+body joined
    assert texts[0] == "refund request email me at about the charge"
