<div align="center">

# Ticket Intel

**NLP Pipeline for Support Ticket Routing and Summarization**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-teal.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

*Fast routing • Auto-summarization • Entity extraction*

**[Live Demo](https://ticket-intel-ccallahan308.streamlit.app/)** — interactive demo on synthetic data

</div>

---

## Problem

Support teams triage large volumes of unstructured tickets by hand: figuring out
which team a ticket belongs to, reading long threads, and pulling out the key
details. Ticket Intel automates the first pass — it **routes** a ticket to a
category, produces an **extractive summary**, and extracts **entities, keywords,
and sentiment** — using a classic, cheap, interpretable ML stack rather than a
large language model.

**Why not an LLM?** For high-volume routing you rarely need GPT-class reasoning
to know that "refund please" is a billing ticket. A TF-IDF + Naive Bayes pipeline
trains in milliseconds, predicts in well under a millisecond per ticket, costs
effectively nothing to run, and is fully interpretable. The router is abstracted
so a transformer can be dropped in later (see [Future Work](#future-work)).

## Dataset

- **Real benchmark — [Banking77](https://huggingface.co/datasets/PolyAI/banking77):**
  13,083 real customer-banking queries labelled with **77 fine-grained intents**
  (`card_arrival`, `card_payment_fee_charged`, `pending_top_up`, …). A widely-cited
  intent-classification benchmark. This is what the reported [results](#results)
  are measured on. It is not committed — see [How to Run](#how-to-run) for the
  download. `src/data/loader.py` auto-detects the `text` / `category` columns.
- **Zero-setup demo:** a balanced **synthetic** set of 90 example tickets in
  `src/models/router.py` (`DEMO_DATA`), used automatically when no dataset is
  present so the API, dashboard, and tests run with no download. Six categories:
  `Account`, `Billing`, `Bug`, `Feature Request`, `General`, `Performance`.

## Methodology

| Component | Approach | Notes |
|-----------|----------|-------|
| Routing | `TfidfVectorizer` (1–2 grams) → `MultinomialNB`, wrapped in an sklearn `Pipeline` | Preprocessing lives inside the Pipeline, so there is no train/test leakage |
| Summarization | Extractive — word-frequency sentence scoring | No hallucination risk; pure stdlib |
| Entity extraction | Rule-based regex (email, money, date, version, error code, URL) | Deterministic, no model |
| Sentiment / keywords | Lexicon polarity + frequency | Lightweight heuristics |
| Evaluation | Stratified out-of-fold cross-validation + a most-frequent-class baseline | `src/models/evaluate.py` |
| API | FastAPI (async) | `/route`, `/summarize`, `/insights`, `/batch`, `/health` |
| UI | Streamlit | `app.py` (single-file demo) and `src/ui/dashboard.py` (full dashboard) |

Hyperparameters and the random seed live in `src/config.py`.

## Results

> Measured with **5-fold stratified out-of-fold cross-validation** — every scored
> prediction is on data the model did not train on — against a most-frequent-class
> baseline. Reproduce with `python -m src.models.evaluate --input tickets.csv`.

**Banking77 — 77-intent classification (13,083 queries):**

| Metric | Model | Most-frequent baseline |
|--------|:-----:|:----------------------:|
| Accuracy | **0.820** | 0.017 |
| Macro F1 | **0.817** | — |
| Weighted F1 | **0.818** | — |

A ~47× lift over the baseline on a genuinely hard 77-class problem, from a plain
TF-IDF + Naive Bayes pipeline. **Error analysis** (per-class F1 in `metrics.json`):
the model nails lexically distinctive intents (`passcode_forgotten` 0.98,
`apple_pay_or_google_pay` 0.97) and struggles where intents overlap
(`pending_top_up` 0.54, `top_up_failed` 0.64) — a sensible, expected failure mode.
Transformer models reach ~0.93 on Banking77, which sets a concrete target for the
transformer upgrade noted in [Future Work](#future-work).

**Zero-setup sanity check (synthetic `DEMO_DATA`, 90 examples):** 0.53 accuracy
vs 0.17 baseline — confirms the pipeline learns signal with no download required
(`python main.py evaluate`).

## How to Run

```bash
git clone https://github.com/CCallahan308/ticket-intel.git
cd ticket-intel

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

python main.py train              # train the router (uses synthetic demo data)
python main.py evaluate           # cross-validate + write metrics.json
python main.py api                # FastAPI server  -> http://localhost:8000/docs
python main.py ui                 # full Streamlit dashboard
streamlit run app.py              # single-file demo app
```

Train/evaluate on the real Banking77 dataset:

```bash
# Download the official train/test splits and combine into tickets.csv
B=https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data
curl -sL $B/train.csv -o b77_train.csv && curl -sL $B/test.csv -o b77_test.csv
python -c "import pandas as pd; pd.concat([pd.read_csv('b77_train.csv'), pd.read_csv('b77_test.csv')]).to_csv('tickets.csv', index=False)"

python src/models/train_router.py --input tickets.csv   # train on real data
python -m src.models.evaluate --input tickets.csv        # -> metrics.json
```

Run the tests:

```bash
pytest -q
```

### Docker

```bash
docker build -t ticket-intel-api -f Dockerfile.api .
docker run -p 8000:8000 ticket-intel-api

docker build -t ticket-intel-ui -f Dockerfile.ui .
docker run -p 8501:8501 ticket-intel-ui
```

## Project structure

```
src/
├── config.py             # paths, hyperparameters, random seed (single source of truth)
├── api/                  # FastAPI routes + Pydantic schemas
├── models/
│   ├── router.py             # TF-IDF + Naive Bayes pipeline (+ saved metadata)
│   ├── summarizer.py         # extractive summarizer
│   ├── insights.py           # regex entities, keywords, sentiment
│   ├── train_router.py       # training CLI
│   ├── evaluate.py           # cross-validation + baseline -> metrics.json
│   └── artifacts/            # saved model + metadata + metrics (git-ignored)
├── data/loader.py        # dataset loading, column detection, text cleaning
└── ui/                   # Streamlit dashboard components
app.py                    # single-file Streamlit demo (wired to the real model)
main.py                   # CLI entry point (api | ui | train | evaluate)
notebooks/01_EDA.ipynb    # exploratory data analysis (run against tickets.csv)
```

## Future Work

- **Transformer router.** `TicketRouter` is abstracted so a fine-tuned
  DistilBERT/RoBERTa classifier could replace TF-IDF+NB when the accuracy budget
  justifies the compute. *(Not yet implemented.)*
- **Hyperparameter search.** The TF-IDF/NB params in `config.py` are sensible
  defaults; `GridSearchCV` on a real dataset would tune them.
- **Class imbalance handling.** Real ticket data is imbalanced; add `class_weight`
  / resampling and report weighted F1.
- **Held-out test set + monitoring** once trained on real data at scale.

## License

MIT
