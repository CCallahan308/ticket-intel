"""Train and save the ticket router model."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.models.router import DEMO_DATA, train_router


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the ticket router")
    parser.add_argument("--input", type=Path, default=None,
                        help="Path to CSV with 'text' and 'category' columns")
    args = parser.parse_args()

    if args.input and args.input.exists():
        import csv
        with args.input.open() as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
        texts = [r["text"] for r in rows]
        labels = [r["category"] for r in rows]
    else:
        print("No input file provided — training on built-in demo data.")
        texts, labels = zip(*DEMO_DATA)
        texts, labels = list(texts), list(labels)

    pipe, l2i, i2l = train_router(texts, labels, save=True)
    print(f"Trained router with {len(set(labels))} categories: {sorted(set(labels))}")
    print("Model saved to src/models/artifacts/router.pkl")


if __name__ == "__main__":
    main()
