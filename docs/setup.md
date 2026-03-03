# Getting Started

This guide covers everything you need to know to run the **Ticket Intel** application locally and in production.

---

## 🐍 Local Python Environment

Start by cloning the repository and setting up your environment:

```bash
# Clone the repo (replace with your fork)
git clone https://github.com/CCallahan308/ticket-intel.git
cd ticket-intel

# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 💾 The Dataset

This project is built for the [Kaggle Customer Support Ticket Dataset](https://www.kaggle.com/datasets/waseemalastal/customer-support-ticket-dataset).
Download the dataset and save it as `tickets.csv` in the root of the project folder.

---

## 🏃‍♂️ Running the Services

Ticket Intel has two main components: an API and a Dashboard. You can run them using the provided CLI tool.

### 1. The FastAPI Backend

Run the intelligent routing and summarization API:

```bash
python main.py api
```

The API will start at `http://localhost:8000`.
✨ **Pro Tip:** Head over to `http://localhost:8000/docs` to interact with the auto-generated Swagger UI!

### 2. The Streamlit Dashboard

Run the interactive visualization UI:

```bash
python main.py ui
```

The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## 🐳 Docker Deployment

Ticket Intel includes production-ready Dockerfiles for both the API and the UI.

### Build and Run API

```bash
docker build -t ticket-intel-api -f Dockerfile.api .
docker run -p 8000:8000 ticket-intel-api
```

### Build and Run UI

```bash
docker build -t ticket-intel-ui -f Dockerfile.ui .
docker run -p 8501:8501 ticket-intel-ui
```

---

## 🧪 Testing and Formatting

We use `pytest` for unit testing and `pre-commit` for maintaining code standard out of the box.

```bash
# Run the test suite
pytest tests/

# Install formatting hooks to ensure commits meet quality thresholds
pre-commit install
```
