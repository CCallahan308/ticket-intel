"""Evaluate the ticket router honestly and persist real metrics.

Uses stratified out-of-fold cross-validation (so every prediction scored is on
data the model did not train on) and compares against a most-frequent-class
baseline. Writes results to ``src/models/artifacts/metrics.json``.

Run:
    python -m src.models.evaluate                 # synthetic demo data
    python -m src.models.evaluate --input tickets.csv   # real dataset
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# Allow direct execution (python src/models/evaluate.py) as well as -m.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import sklearn
from sklearn.dummy import DummyClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.preprocessing import LabelEncoder

from src import config
from src.models.router import DEMO_DATA, _build_pipeline

logger = logging.getLogger(__name__)


def _load_data(input_path: Path | None) -> tuple[list[str], list[str], str]:
    """Return (texts, labels, source_description)."""
    if input_path is not None and input_path.exists():
        from src.data.loader import load_labeled_tickets

        texts, labels = load_labeled_tickets(input_path)
        return texts, labels, str(input_path)

    texts, labels = zip(*DEMO_DATA)
    return list(texts), list(labels), "synthetic demo data"


def evaluate(input_path: Path | None = None) -> dict:
    """Cross-validate the router, compare to a baseline, and write metrics.json."""
    texts, labels, source = _load_data(input_path)

    le = LabelEncoder()
    y = le.fit_transform(labels)
    target_names = list(le.classes_)

    # Stratified CV needs n_splits <= the smallest class count.
    min_class = min(Counter(labels).values())
    n_splits = max(2, min(config.CV_FOLDS, min_class))
    if min_class < config.CV_FOLDS:
        logger.warning(
            "Smallest class has %d samples; reducing CV folds to %d.",
            min_class,
            n_splits,
        )
    skf = StratifiedKFold(
        n_splits=n_splits, shuffle=True, random_state=config.RANDOM_STATE
    )

    y_pred = cross_val_predict(_build_pipeline(), texts, y, cv=skf)

    # Most-frequent-class baseline (X is ignored by this strategy).
    dummy_x = np.zeros((len(texts), 1))
    y_base = cross_val_predict(
        DummyClassifier(strategy="most_frequent"), dummy_x, y, cv=skf
    )

    report = classification_report(
        y, y_pred, target_names=target_names, output_dict=True, zero_division=0
    )
    text_report = classification_report(
        y, y_pred, target_names=target_names, zero_division=0
    )
    cm = confusion_matrix(y, y_pred).tolist()
    baseline_acc = float((y_base == y).mean())

    metrics = {
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "data_source": source,
        "evaluation": f"stratified {n_splits}-fold out-of-fold cross-validation",
        "n_samples": len(texts),
        "n_classes": len(target_names),
        "categories": target_names,
        "random_state": config.RANDOM_STATE,
        "sklearn_version": sklearn.__version__,
        "model": {
            "accuracy": report["accuracy"],
            "macro_f1": report["macro avg"]["f1-score"],
            "weighted_f1": report["weighted avg"]["f1-score"],
        },
        "baseline_most_frequent": {"accuracy": baseline_acc},
        "per_class": {name: report[name] for name in target_names},
        "confusion_matrix": {"labels": target_names, "matrix": cm},
    }

    config.METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    config.METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    logger.info("Evaluation on %s (%d samples)", source, len(texts))
    logger.info("\n%s", text_report)
    logger.info(
        "Model accuracy %.3f vs most-frequent baseline %.3f (macro-F1 %.3f)",
        metrics["model"]["accuracy"],
        baseline_acc,
        metrics["model"]["macro_f1"],
    )
    logger.info("Metrics written to %s", config.METRICS_PATH)
    return metrics


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Evaluate the ticket router")
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="CSV with 'text' and 'category' columns (defaults to demo data)",
    )
    args = parser.parse_args()
    evaluate(args.input)


if __name__ == "__main__":
    main()
