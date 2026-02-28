# Ticket Intel

NLP system for support ticket routing, summarization, and insight extraction.

![Python](https://img.shields.io/badge/Python-3.9%2B-teal)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-teal)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-teal)

## What it does

- **Routing** - Classifies tickets into categories using TF-IDF + Naive Bayes (Modularized for future Transformer upgrades)
- **Summarization** - Extractive summaries via sentence scoring
- **Insights** - Entity extraction, keywords, sentiment detection
- **API** - FastAPI endpoints with OpenAPI docs
- **Dashboard** - Streamlit UI with visualizations and batch processing

Built for the [Kaggle Customer Support Dataset](https://www.kaggle.com/datasets/waseemalastal/customer-support-ticket-dataset)

## Quick Start

### Local Development

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

Download the dataset from Kaggle, save as `tickets.csv` in the project folder.

**API:**

```bash
python main.py api
# Docs at http://localhost:8000/docs
```

**Dashboard:**

```bash
python main.py ui
```

### Docker Deployment

```bash
# Build and run API
docker build -t ticket-intel-api -f Dockerfile.api .
docker run -p 8000:8000 ticket-intel-api

# Build and run UI
docker build -t ticket-intel-ui -f Dockerfile.ui .
docker run -p 8501:8501 ticket-intel-ui
```

## Project Structure

```text
ticket-intel/
├── .github/workflows/ # CI/CD pipelines
├── notebooks/         # Exploratory Data Analysis
├── src/
│   ├── api/           # FastAPI application & routers
│   ├── data/          # Data loading and preprocessing pipelines
│   ├── models/        # ML models (Router, Summarizer, Insights)
│   ├── ui/            # Streamlit dashboard and charts
│   └── utils/         # Shared utilities (NLP ops, etc.)
├── tests/             # Pytest suite
├── main.py            # CLI entrypoint
├── Dockerfile.api     # Production API image
├── Dockerfile.ui      # Production UI image
├── requirements.txt
└── README.md
```

## Testing & Quality Assurance

This project uses `pytest` for unit testing and `pre-commit` for code formatting.

```bash
# Run tests
pytest tests/

# Install pre-commit hooks
pre-commit install
```

## License

MIT
