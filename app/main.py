from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from app.core.config import APP_ENV, APP_NAME, APP_VERSION

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="REST API for uploading documents and asking questions about them (RAG).",
)


class EchoRequest(BaseModel):
    message: str

class NoteCreate(BaseModel):
    title: str = Field (..., min_length=3, max_length=100)
    content: Optional[str] = None

@app.get("/")
def root():
    return {"name": APP_NAME, "version": APP_VERSION, "env": APP_ENV, "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/items")
def list_items(limit: int = Query(10, ge=1, le=50), keyword: Optional[str] = None):        
    return {"limit": limit, "keyword": keyword}

@app.post("/echo")
def echo(payload: EchoRequest):
    return {"echo": payload.message}

@app.post("/notes", status_code=201)
def create_note(payload: NoteCreate):
    return {
        "title": payload.title,
        "content": payload.content
    }
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