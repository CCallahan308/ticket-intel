import re
import string
from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd

PKG_DIR = Path(__file__).parent.parent.parent

COL_VARIANTS = {
    "subj": ["Ticket Subject", "Subject", "subject", "title"],
    "body": ["Ticket Description", "Body", "body", "text", "message"],
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


def load_tickets(fp: Path = None) -> pd.DataFrame:
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
    df.attrs["subj"] = find_column(df, "subj")
    df.attrs["body"] = find_column(df, "body")
    df.attrs["cat"] = find_column(df, "cat")

    return df
