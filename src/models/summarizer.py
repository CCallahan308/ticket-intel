"""Extractive ticket summarizer using sentence scoring."""

from __future__ import annotations

import re
from collections import Counter


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def _word_freq(text: str) -> Counter:
    words = re.findall(r"\b[a-z]{3,}\b", text.lower())
    stop = {
        "the",
        "and",
        "for",
        "that",
        "this",
        "with",
        "are",
        "was",
        "have",
        "not",
        "but",
        "from",
        "you",
        "your",
        "our",
        "can",
        "has",
        "been",
    }
    return Counter(w for w in words if w not in stop)


def summarize(text: str, n: int = 2) -> tuple[str, int]:
    """Return an extractive summary of *text*.

    Returns (summary, sentence_count).
    """
    if not text or not text.strip():
        return "", 0
    sents = _sentences(text)
    if len(sents) <= n:
        return text.strip(), len(sents)

    freq = _word_freq(text)
    scores = []
    for sent in sents:
        words = re.findall(r"\b[a-z]{3,}\b", sent.lower())
        score = sum(freq[w] for w in words) / max(len(words), 1)
        scores.append(score)

    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n]
    top_indices.sort()
    result = " ".join(sents[i] for i in top_indices)
    return result, len(top_indices)
