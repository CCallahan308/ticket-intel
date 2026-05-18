<div align="center">
  
# Ticket Intel

**NLP Pipeline for Support Ticket Routing and Summarization**

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-teal.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

*Fast routing • Auto-summarization • Entity extraction*

**[Live Demo](https://ticket-intel-ccallahan308.streamlit.app/)** - Try the interactive demo

</div>

---

## What this does

Routes support tickets to the right team, summarizes long threads, and extracts key entities. Built for speed - 12ms p99 latency per ticket.

Why not use LLMs? Because in high-volume support queues, you don't need GPT-4 to know that "refund please" goes to the billing team. TF-IDF + Naive Bayes handles 500+ req/sec for pennies.

## Architecture

| Component | Tech | Purpose |
|-----------|------|---------|
| Routing | TF-IDF + MultinomialNB | Classify ticket into 5 categories |
| Summarization | Extractive (TF-IDF) | Pull key sentences from long threads |
| Entity Extraction | Rule-based regex NER | Pull versions, error codes, URLs, emails |
| API | FastAPI | Async endpoints, 500+ req/sec |
| UI | Streamlit | Batch processing dashboard |

## Benchmarks

Tested on AWS t3.medium:

| Category | Precision | Recall | F1 |
|:---------|:---------:|:------:|:--:|
| Refund request | 0.91 | 0.89 | 0.90 |
| Technical issue | 0.88 | 0.92 | 0.90 |
| Cancellation | 0.93 | 0.90 | 0.91 |
| Product inquiry | 0.89 | 0.87 | 0.88 |
| Billing inquiry | 0.90 | 0.91 | 0.90 |

**Latency:** 12ms p99 per ticket

## Extending to Transformers

The router is abstracted so you can swap in BERT/RoBERTa when you have the compute budget:

```python
from src.models.router import TicketRouter
from transformers import pipeline

class TransformerRouter(TicketRouter):
    def __init__(self, model_name="distilbert-base-uncased"):
        self.classifier = pipeline("text-classification", model=model_name)
    
    def predict(self, text: str) -> str:
        return self.classifier(text)[0]['label']
```

## Quick start

```bash
# clone the repo
git clone https://github.com/CCallahan308/ticket-intel.git
cd ticket-intel

# set up virtualenv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# train the routing model (uses built-in demo data if no CSV provided)
python src/models/train_router.py

# run the FastAPI server
python main.py api

# run the Streamlit dashboard (full batch-processing UI)
python main.py ui

# or launch the simplified demo app directly
streamlit run app.py
```

API docs at `http://localhost:8000/docs`

### Optional: load a real dataset

```bash
kaggle datasets download -d waseemalastal/customer-support-ticket-dataset
unzip customer-support-ticket-dataset.zip -d .
mv customer_support_tickets.csv tickets.csv
```

## Docker

```bash
docker build -t ticket-intel-api -f Dockerfile.api .
docker run -p 8000:8000 ticket-intel-api

docker build -t ticket-intel-ui -f Dockerfile.ui .
docker run -p 8501:8501 ticket-intel-ui
```

## Repo structure

```
├── src/
│   ├── api/              # FastAPI routes and Pydantic schemas
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── models/           # ML pipeline: routing, summarization, insights
│   │   ├── router.py         # TF-IDF + Naive Bayes classifier
│   │   ├── summarizer.py     # Extractive text summarizer
│   │   ├── insights.py       # Entity extraction, keywords, sentiment
│   │   ├── train_router.py   # Training script (CLI)
│   │   └── artifacts/        # Saved model files (git-ignored)
│   ├── data/             # Dataset loaders and text cleaning
│   │   └── loader.py
│   └── ui/               # Streamlit dashboard components
│       ├── dashboard.py      # Main dashboard (full-featured)
│       ├── charts.py         # Plotly chart builders
│       └── styles.py         # CSS theme and HTML helpers
├── tests/
├── app.py                # Simplified Streamlit demo
├── main.py               # CLI entry point for FastAPI server
├── Dockerfile.api
├── Dockerfile.ui
└── requirements.txt
```

> **Note:** `app.py` is a lightweight demo app suitable for quick exploration.
> `main.py` is the full production entry point that starts the FastAPI server
> with the lifespan-managed model loader.

## License

MIT
