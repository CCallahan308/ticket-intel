"""Central configuration: paths, model hyperparameters, and reproducibility seeds.

Single source of truth so constants are not scattered across modules.
"""

from __future__ import annotations

from pathlib import Path

# --- Reproducibility -------------------------------------------------------
RANDOM_STATE: int = 42

# --- Paths -----------------------------------------------------------------
PKG_ROOT: Path = Path(__file__).resolve().parent  # .../src
PROJECT_ROOT: Path = PKG_ROOT.parent  # repo root
ARTIFACTS_DIR: Path = PKG_ROOT / "models" / "artifacts"
MODEL_PATH: Path = ARTIFACTS_DIR / "router.pkl"
LABEL_PATH: Path = ARTIFACTS_DIR / "labels.json"
METADATA_PATH: Path = ARTIFACTS_DIR / "metadata.json"
METRICS_PATH: Path = ARTIFACTS_DIR / "metrics.json"

# --- Router hyperparameters ------------------------------------------------
# Defaults chosen for a fast, interpretable baseline. On a real dataset these
# should be tuned with GridSearchCV (see Future Work in the README).
TFIDF_NGRAM_RANGE: tuple[int, int] = (1, 2)
TFIDF_MAX_FEATURES: int = 5000
TFIDF_SUBLINEAR_TF: bool = True
TFIDF_STOP_WORDS: str = "english"
NB_ALPHA: float = 0.1

# --- Evaluation ------------------------------------------------------------
CV_FOLDS: int = 5  # capped to the smallest class count at runtime
TEST_SIZE: float = 0.2  # held-out fraction when a real dataset is provided
