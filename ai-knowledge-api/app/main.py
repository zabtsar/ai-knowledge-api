from fastapi import FastAPI
from pydantic import BaseModel

from app.core.config import APP_ENV, APP_NAME, APP_VERSION

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="REST API for uploading documents and asking questions about them (RAG).",
)


class EchoRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"name": APP_NAME, "version": APP_VERSION, "env": APP_ENV, "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/echo")
def echo(payload: EchoRequest):
    return {"echo": payload.message}
