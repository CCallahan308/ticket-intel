from fastapi.testclient import TestClient
from src.api.routes import router
from fastapi import FastAPI

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
