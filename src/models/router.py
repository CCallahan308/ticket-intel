"""TF-IDF + Multinomial Naive Bayes ticket router."""
from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

_MODEL_PATH = Path(__file__).parent / "artifacts" / "router.pkl"
_LABEL_PATH = Path(__file__).parent / "artifacts" / "labels.json"

DEMO_DATA = [
    ("App crashes on login page", "Bug"),
    ("Login button not working after update", "Bug"),
    ("Error 500 when submitting form", "Bug"),
    ("Screen goes blank on mobile", "Bug"),
    ("How do I reset my password?", "Account"),
    ("Can't access my account after email change", "Account"),
    ("Update billing information", "Billing"),
    ("Charge appears twice on my statement", "Billing"),
    ("Cancel my subscription please", "Billing"),
    ("Feature request: dark mode support", "Feature Request"),
    ("Would love an export to CSV option", "Feature Request"),
    ("Add keyboard shortcuts to the editor", "Feature Request"),
    ("How does the search feature work?", "General"),
    ("What are your business hours?", "General"),
    ("Performance is slow today", "Performance"),
    ("Page takes 30 seconds to load", "Performance"),
    ("API response time degraded", "Performance"),
]


def _build_pipeline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000,
            sublinear_tf=True,
            stop_words="english",
        )),
        ("clf", MultinomialNB(alpha=0.1)),
    ])


def train_router(
    texts: list[str],
    labels: list[str],
    save: bool = True,
) -> tuple[Pipeline, dict[str, int], dict[int, str]]:
    """Train the router pipeline and optionally persist it.

    Returns (pipe, l2i, i2l) where l2i maps label->index and i2l maps index->label.
    """
    le = LabelEncoder()
    y = le.fit_transform(labels)
    i2l: dict[int, str] = {i: label for i, label in enumerate(le.classes_)}
    l2i: dict[str, int] = {label: i for i, label in i2l.items()}

    pipe = _build_pipeline()
    pipe.fit(texts, y)

    if save:
        _MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _MODEL_PATH.open("wb") as fh:
            pickle.dump((pipe, l2i, i2l), fh)
        with _LABEL_PATH.open("w") as fh:
            json.dump({str(k): v for k, v in i2l.items()}, fh)

    return pipe, l2i, i2l


def load_router() -> tuple[Pipeline, dict[str, int], dict[int, str]]:
    """Load router from disk, training on demo data if not yet saved.

    Returns (pipe, l2i, i2l).
    """
    if _MODEL_PATH.exists():
        with _MODEL_PATH.open("rb") as fh:
            pipe, l2i, i2l = pickle.load(fh)  # noqa: S301 — trusted local artifact
        return pipe, l2i, i2l
    texts, labels = zip(*DEMO_DATA)
    return train_router(list(texts), list(labels), save=True)


def route(
    text: str,
    pipe: Any,
    i2l: dict[int, str],
) -> tuple[str, float, dict[str, float]]:
    """Route a single ticket text.

    Returns (category, confidence, all_probabilities).
    """
    default_label = i2l.get(0, "General")
    if not text or not text.strip():
        return default_label, 0.0, {default_label: 1.0}

    proba = pipe.predict_proba([text])[0]
    idx = int(np.argmax(proba))
    category = i2l.get(idx, "General")
    confidence = float(proba[idx])
    all_probs = {i2l.get(i, str(i)): float(p) for i, p in enumerate(proba)}
    return category, confidence, all_probs
