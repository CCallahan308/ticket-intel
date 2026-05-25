"""TF-IDF + Multinomial Naive Bayes ticket router."""

from __future__ import annotations

import json
import pickle
from datetime import datetime, timezone

import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

from src import config

_MODEL_PATH = config.MODEL_PATH
_LABEL_PATH = config.LABEL_PATH
_METADATA_PATH = config.METADATA_PATH

# Balanced, clearly-synthetic demo set (15 examples per category) used when no
# real dataset is provided. It is large enough for the pipeline to learn real
# lexical signal so the demo classifies meaningfully — but it is NOT a benchmark
# dataset. For real numbers, train/evaluate on the Kaggle support-ticket dataset.
DEMO_DATA = [
    # Bug
    ("App crashes on login page", "Bug"),
    ("Login button not working after the latest update", "Bug"),
    ("Error 500 when submitting the contact form", "Bug"),
    ("Screen goes blank on mobile after I tap save", "Bug"),
    ("The export feature throws an exception every time", "Bug"),
    ("Uploading a file fails with a network error", "Bug"),
    ("Dashboard charts fail to render in Safari", "Bug"),
    ("Notifications stopped working since version 2.3", "Bug"),
    ("Clicking submit does nothing, the page just freezes", "Bug"),
    ("App keeps logging me out unexpectedly", "Bug"),
    ("Search returns a blank page instead of results", "Bug"),
    ("The mobile app crashes immediately on startup", "Bug"),
    ("Getting a 404 when opening shared links", "Bug"),
    ("Form validation is broken and rejects valid emails", "Bug"),
    ("Images are not loading in the gallery view", "Bug"),
    # Account
    ("How do I reset my password?", "Account"),
    ("Can't access my account after changing my email", "Account"),
    ("I need to update the email address on my profile", "Account"),
    ("Two-factor authentication code never arrives", "Account"),
    ("Locked out of my account after too many attempts", "Account"),
    ("How do I change my username?", "Account"),
    ("I want to delete my account permanently", "Account"),
    ("Unable to log in even with the correct password", "Account"),
    ("How do I add a teammate to my workspace?", "Account"),
    ("My profile picture won't update", "Account"),
    ("I forgot which email I used to sign up", "Account"),
    ("How do I enable single sign-on for my team?", "Account"),
    ("Need to transfer account ownership to a colleague", "Account"),
    ("Where can I update my notification preferences?", "Account"),
    ("How do I merge two accounts into one?", "Account"),
    # Billing
    ("Update my billing information", "Billing"),
    ("There is a duplicate charge on my statement", "Billing"),
    ("Please cancel my subscription", "Billing"),
    ("I was charged after I already cancelled", "Billing"),
    ("Can I get a refund for this month?", "Billing"),
    ("Where do I download my invoice?", "Billing"),
    ("My card was declined but I was still charged", "Billing"),
    ("How do I switch from monthly to annual billing?", "Billing"),
    ("Requesting a refund for the duplicate payment", "Billing"),
    ("Update the credit card on file", "Billing"),
    ("Why did my subscription price increase?", "Billing"),
    ("I need a receipt for my last payment", "Billing"),
    ("How do I apply a coupon to my subscription?", "Billing"),
    ("Cancel my plan and stop future charges", "Billing"),
    ("I was billed in the wrong currency", "Billing"),
    # Feature Request
    ("Feature request: dark mode support", "Feature Request"),
    ("Would love an export to CSV option", "Feature Request"),
    ("Add keyboard shortcuts to the editor", "Feature Request"),
    ("Please add support for authenticator-app two-factor", "Feature Request"),
    ("It would be great to have a native mobile app", "Feature Request"),
    ("Can you add bulk delete for old tickets?", "Feature Request"),
    ("Requesting an integration with Slack", "Feature Request"),
    ("Add the ability to schedule recurring reports", "Feature Request"),
    ("Please support custom tags on tickets", "Feature Request"),
    ("Would be nice to have a calendar view", "Feature Request"),
    ("Add an option to duplicate a project", "Feature Request"),
    ("Can we get webhook support for new events?", "Feature Request"),
    ("Please allow exporting charts as images", "Feature Request"),
    ("Add a way to favorite frequently used items", "Feature Request"),
    ("It would help to have role-based permissions", "Feature Request"),
    # General
    ("How does the search feature work?", "General"),
    ("What are your business hours?", "General"),
    ("Do you offer a free trial?", "General"),
    ("Where can I find the documentation?", "General"),
    ("Is my data stored securely?", "General"),
    ("What payment methods do you accept?", "General"),
    ("How do I contact your support team?", "General"),
    ("Do you have a status page for outages?", "General"),
    ("Can I use this for my whole company?", "General"),
    ("What is included in the free plan?", "General"),
    ("Where are your servers located?", "General"),
    ("How often do you release updates?", "General"),
    ("Do you have an affiliate program?", "General"),
    ("Is there a limit on the number of projects?", "General"),
    ("What languages does the product support?", "General"),
    # Performance
    ("Performance is slow today", "Performance"),
    ("The page takes 30 seconds to load", "Performance"),
    ("API response time has degraded significantly", "Performance"),
    ("The dashboard is laggy when I have many tickets", "Performance"),
    ("Search is extremely slow on large datasets", "Performance"),
    ("Reports time out before they finish generating", "Performance"),
    ("The app freezes for several seconds when switching tabs", "Performance"),
    ("Loading the inbox is much slower than last week", "Performance"),
    ("Exports are taking far too long to complete", "Performance"),
    ("There is noticeable lag when typing in the editor", "Performance"),
    ("The site becomes unresponsive during peak hours", "Performance"),
    ("Uploading large files is painfully slow", "Performance"),
    ("Page load times have gotten worse after the update", "Performance"),
    ("Syncing data takes minutes instead of seconds", "Performance"),
    ("The API frequently times out under load", "Performance"),
]


def _build_pipeline() -> Pipeline:
    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=config.TFIDF_NGRAM_RANGE,
                    max_features=config.TFIDF_MAX_FEATURES,
                    sublinear_tf=config.TFIDF_SUBLINEAR_TF,
                    stop_words=config.TFIDF_STOP_WORDS,
                ),
            ),
            ("clf", MultinomialNB(alpha=config.NB_ALPHA)),
        ]
    )


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
        _write_metadata(texts, i2l)

    return pipe, l2i, i2l


def _write_metadata(texts: list[str], i2l: dict[int, str]) -> None:
    """Persist model lineage alongside the pickle for traceability."""
    metadata = {
        "model_type": "TfidfVectorizer + MultinomialNB",
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "n_samples": len(texts),
        "n_categories": len(i2l),
        "categories": [i2l[i] for i in sorted(i2l)],
        "sklearn_version": sklearn.__version__,
        "hyperparameters": {
            "tfidf_ngram_range": list(config.TFIDF_NGRAM_RANGE),
            "tfidf_max_features": config.TFIDF_MAX_FEATURES,
            "tfidf_sublinear_tf": config.TFIDF_SUBLINEAR_TF,
            "nb_alpha": config.NB_ALPHA,
        },
    }
    with _METADATA_PATH.open("w") as fh:
        json.dump(metadata, fh, indent=2)


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
    pipe: Pipeline,
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
