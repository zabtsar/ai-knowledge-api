# AI Knowledge API

A REST API where users upload documents and ask questions about them, answered with Retrieval-Augmented Generation (RAG).

**Status:** in development. Built step by step over 13 weeks (Nov 2026 - Feb 2027).

## Planned features

- [x] Project skeleton and basic endpoints
- [x] CRUD for documents (FastAPI + PostgreSQL)
- [ ] JWT authentication and role-based access (admin/user)
- [ ] Security hardening (rate limiting, input validation, CORS)
- [ ] RAG pipeline: ingest, split, embed, vector search, chat with memory and source citations
- [ ] Dockerized setup (`docker compose up`)
- [ ] CI/CD with GitHub Actions
- [ ] Public deployment on AWS with HTTPS

## Tech stack

Python, FastAPI, Pydantic, PostgreSQL, SQLAlchemy, pytest. Planned: Docker, GitHub Actions, AWS, a vector database (AstraDB or pgvector), an LLM API.

## Getting started

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env

# 4. Run the API
uvicorn app.main:app --reload

# 5. Set up PostgreSQL
#    Install PostgreSQL, create a database, then copy .env.example to .env
#    and fill in DATABASE_URL (never commit .env)
copy .env.example .env           # macOS/Linux: cp .env.example .env

# 6. Create the tables
python create_tables.py
```

Open http://127.0.0.1:8000/docs for the interactive API documentation.

## Run tests

```bash
pytest
```

## Project structure

```
ai-knowledge-api/
├── app/
│   ├── main.py          # FastAPI app and endpoints
│   ├── database.py      # Database engine and session
│   ├── models.py        # SQLAlchemy models (User, Document)
│   ├── schemas.py       # Pydantic schemas
│   ├── api/routes/      # Route modules (planned)
│   ├── core/            # Config and security helpers
│   ├── db/              # Database helpers (planned)
│   └── services/        # Business logic (planned)
├── tests/
│   ├── conftest.py      # Shared test fixtures
│   ├── test_main.py     # Basic endpoint tests
│   └── test_documents.py  # Document CRUD tests
├── docs/                # Notes, diagrams, screenshots
├── create_tables.py     # Creates database tables
├── test_connection.py   # Checks the database connection
├── .env.example         # Environment variable template
└── requirements.txt
```

## Author

Zidan Absar Abdallah - [GitHub](https://github.com/zabtsar) - [LinkedIn](https://linkedin.com/in/zidanabsarabdallah)
