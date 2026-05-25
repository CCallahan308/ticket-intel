from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.api.routes import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"


def test_route_model_not_loaded(monkeypatch):
    from src.api.routes import state

    monkeypatch.setattr(state, "pipe", None)

    response = client.post("/route", json={"subject": "test", "body": "test"})
    assert response.status_code == 503


def test_route_success(monkeypatch):
    from src.api.routes import state

    class DummyPipe:
        def predict_proba(self, X):
            import numpy as np

            return np.array([[0.1, 0.9]])

    monkeypatch.setattr(state, "pipe", DummyPipe())
    monkeypatch.setattr(state, "i2l", {0: "A", 1: "B"})

    response = client.post("/route", json={"subject": "test", "body": "test body"})
    assert response.status_code == 200
    assert response.json()["category"] == "B"


def test_summarize_endpoint():
    response = client.post(
        "/summarize",
        json={"subject": "Short", "body": "This is very short and simple text."},
    )
    assert response.status_code == 200
    assert "summary" in response.json()


def test_insights_endpoint():
    response = client.post(
        "/insights",
        json={"subject": "Issue", "body": "I have an issue with order #12345"},
    )
    assert response.status_code == 200
    assert "sentiment" in response.json()
