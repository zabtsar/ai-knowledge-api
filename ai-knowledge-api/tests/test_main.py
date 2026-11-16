from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_echo():
    response = client.post("/echo", json={"message": "hello"})
    assert response.status_code == 200
    assert response.json() == {"echo": "hello"}


def test_echo_validation_error():
    response = client.post("/echo", json={})
    assert response.status_code == 422
