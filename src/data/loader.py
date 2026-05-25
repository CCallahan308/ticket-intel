from __future__ import annotations

import re
import string
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

PKG_DIR = Path(__file__).parent.parent.parent

COL_VARIANTS = {
    "subj": ["Ticket Subject", "Subject", "subject", "title"],
    "body": ["Ticket Description", "Body", "body", "text", "message",
             "instruction", "utterance", "query"],
    "cat": ["Ticket Type", "Category", "category", "type", "label"],
}


def find_column(df: pd.DataFrame, kind: str) -> Optional[str]:
    opts = COL_VARIANTS.get(kind, [])
    for c in opts:
        if c in df.columns:
            return c
    # fuzzy match
    for col in df.columns:
        kl = kind.lower()
        cl = col.lower()
        if kl in cl or any(k in cl for k in kl.split()):
            return col
    return None


def clean_text(txt: str) -> str:
    if not txt or (isinstance(txt, float) and np.isnan(txt)):
        return ""
    t = str(txt).lower()
    t = re.sub(r"http\S+", "", t)  # urls
    t = re.sub(r"\S+@\S+\.\S+", "", t)  # emails
    t = re.sub(r"\{product_purchased\}", "", t)  # kaggle dataset artifacts
    t = re.sub(r"\d{3}[-.]?\d{3}[-.]?\d{4}", "", t)  # phones
    t = t.translate(str.maketrans("", "", string.punctuation))
    t = re.sub(r"\s+", " ", t).strip()
    return t


def load_tickets(fp: Optional[Path] = None) -> pd.DataFrame:
    if fp is None:
        fp = PKG_DIR / "tickets.csv"

    if not fp.exists():
        for alt in ["support_tickets.csv", "customer_support_tickets.csv", "data.csv"]:
            candidate = PKG_DIR / alt
            if candidate.exists():
                fp = candidate
                break
        else:
            raise FileNotFoundError(
                "No dataset found. Download from:\n"
                "https://www.kaggle.com/datasets/waseemalastal/customer-support-ticket-dataset\n"
                "Save as tickets.csv"
            )

    df = pd.read_csv(fp)
    if df.empty:
        raise ValueError(f"{fp} contains no rows")

    df.attrs["subj"] = find_column(df, "subj")
    df.attrs["body"] = find_column(df, "body")
    df.attrs["cat"] = find_column(df, "cat")

    if df.attrs["subj"] is None and df.attrs["body"] is None:
        raise ValueError(
            f"{fp} has no recognizable subject/body column; "
            f"found columns: {list(df.columns)}"
        )

    return df


def load_labeled_tickets(fp: Path) -> tuple[list[str], list[str]]:
    """Load ``(texts, labels)`` for training/evaluation from a CSV.

    Supports both the simple ``text``/``category`` schema and the Kaggle
    subject/description/type schema — columns are auto-detected, subject and
    body are concatenated and cleaned, and rows with no label or empty text
    are dropped.
    """
    if not fp.exists():
        raise FileNotFoundError(f"{fp} not found")
    df = pd.read_csv(fp)
    if df.empty:
        raise ValueError(f"{fp} contains no rows")

    if {"text", "category"} <= set(df.columns):
        texts = df["text"].astype(str)
        labels = df["category"]
    else:
        subj, body, cat = (find_column(df, k) for k in ("subj", "body", "cat"))
        if cat is None or (subj is None and body is None):
            raise ValueError(
                f"{fp}: need a category column and at least one of subject/body. "
                f"Columns present: {list(df.columns)}"
            )
        combined = None
        for col in (subj, body):
            if col is None:
                continue
            part = df[col].astype(str)
            combined = part if combined is None else combined.str.cat(part, sep=" ")
        texts = combined.map(clean_text)
        labels = df[cat]

    mask = labels.notna() & texts.astype(str).str.strip().astype(bool)
    texts_out = texts[mask].astype(str).tolist()
    labels_out = labels[mask].astype(str).tolist()
    if not texts_out:
        raise ValueError(f"{fp}: no usable rows after cleaning")
    return texts_out, labels_out
