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

def test_hello_zidan():
    response = client.get("/hello/Zidan")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Zidan!"}


def test_items_limit_too_high():
    response = client.get("/items?limit=100")

    assert response.status_code == 422


def test_create_note_title_too_short():
    response = client.post(
        "/notes",
        json={
            "title": "ab",
            "content": "Belajar FastAPI"
        }
    )

    assert response.status_code == 422


def test_create_note_valid():
    response = client.post(
        "/notes",
        json={
            "title": "Belajar FastAPI",
            "content": "Mempelajari pytest"
        }
    )

    assert response.status_code == 201
    assert response.json() == {
        "title": "Belajar FastAPI",
        "content": "Mempelajari pytest"
    }

def test_cors_allowed_origin(client):
    response = client.get(
        "/health",
        headers={
            "Origin": "http://localhost:5173"
        }
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_cors_disallowed_origin(client):
    response = client.get(
        "/health",
        headers={
            "Origin": "http://malicious-site.com"
        }
    )

    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers