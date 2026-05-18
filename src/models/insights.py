"""NLP insights: entities, keywords, and sentiment for support tickets."""
from __future__ import annotations

import re
from collections import Counter


_STOP_WORDS = {
    "the", "and", "for", "that", "this", "with", "are", "was", "have", "not",
    "but", "from", "you", "your", "our", "can", "has", "been", "will", "also",
    "its", "all", "just", "more", "when", "what", "how", "why", "where", "who",
    "get", "got", "does", "did", "any", "one", "two",
}

_POSITIVE = {"thank", "thanks", "great", "awesome", "excellent", "love",
             "perfect", "good", "helpful", "appreciate", "resolved", "fixed",
             "working", "wonderful"}
_NEGATIVE = {"error", "bug", "crash", "broken", "fail", "failed", "failure",
             "issue", "problem", "wrong", "slow", "bad", "terrible", "annoying",
             "frustrating", "upset", "angry", "worst", "unusable", "stuck",
             "awful"}


def extract_keywords(text: str, top_n: int = 5) -> list[str]:
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    counts = Counter(w for w in words if w not in _STOP_WORDS)
    return [w for w, _ in counts.most_common(top_n)]


def extract_entities(text: str) -> list[dict[str, str]]:
    """Rule-based entity extraction (version numbers, error codes, URLs, emails, money, dates)."""
    entities: list[dict[str, str]] = []
    for m in re.finditer(r"\S+@\S+\.\S+", text):
        entities.append({"text": m.group(), "type": "EMAIL"})
    for m in re.finditer(r"\$[\d,]+(?:\.\d{2})?", text):
        entities.append({"text": m.group(), "type": "MONEY"})
    for m in re.finditer(
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b",
        text,
    ):
        entities.append({"text": m.group(), "type": "DATE"})
    for m in re.finditer(r"v?\d+\.\d+(?:\.\d+)?", text):
        entities.append({"text": m.group(), "type": "VERSION"})
    for m in re.finditer(r"\b[A-Z]{2,}\s*\d{3,}\b", text):
        entities.append({"text": m.group(), "type": "ERROR_CODE"})
    for m in re.finditer(r"https?://\S+", text):
        entities.append({"text": m.group(), "type": "URL"})
    return entities


def detect_sentiment(text: str) -> str:
    """Return sentiment label: 'positive', 'negative', or 'neutral'."""
    words = set(re.findall(r"\b[a-z]+\b", text.lower()))
    pos = len(words & _POSITIVE)
    neg = len(words & _NEGATIVE)
    total = pos + neg or 1
    score = (pos - neg) / total
    if score > 0.1:
        return "positive"
    elif score < -0.1:
        return "negative"
    return "neutral"


def insights(text: str) -> tuple[list[dict[str, str]], list[str], str]:
    """Return combined NLP insights for a support ticket.

    Returns (entities, keywords, sentiment).
    """
    sentiment = detect_sentiment(text)
    return (
        extract_entities(text),
        extract_keywords(text),
        sentiment,
    )
