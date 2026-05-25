"""Train and save the ticket router model."""

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.models.router import DEMO_DATA, train_router

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Train the ticket router")
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Path to CSV with 'text' and 'category' columns",
    )
    args = parser.parse_args()

    if args.input and args.input.exists():
        from src.data.loader import load_labeled_tickets

        texts, labels = load_labeled_tickets(args.input)
        logger.info("Training on %s (%d rows)", args.input, len(texts))
    else:
        logger.info("No input file provided - training on built-in demo data.")
        texts, labels = zip(*DEMO_DATA)
        texts, labels = list(texts), list(labels)

    train_router(texts, labels, save=True)
    logger.info(
        "Trained router with %d categories: %s",
        len(set(labels)),
        sorted(set(labels)),
    )
    logger.info("Model + metadata saved to src/models/artifacts/")


if __name__ == "__main__":
    main()
