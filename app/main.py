from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

from app.security import hash_password, verify_password
from app.auth import create_access_token

from app.auth import get_current_user

from app.auth import require_role

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

@app.post(
    "/documents",
    response_model=schemas.DocumentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_document(
    document: schemas.DocumentCreate,
    db: Session = Depends(get_db)
):
    new_document = models.Document(**document.model_dump())

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document

@app.get(
    "/documents",
    response_model=List[schemas.DocumentResponse]
)
def get_documents(db: Session = Depends(get_db)):
    documents = db.query(models.Document).all()

    return documents

@app.get(
    "/documents/{document_id}",
    response_model=schemas.DocumentResponse
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = db.query(models.Document).filter(
        models.Document.id == document_id
    ).first()

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return document

@app.patch(
    "/documents/{document_id}",
    response_model=schemas.DocumentResponse
)
def update_document(
    document_id: int,
    document_data: schemas.DocumentUpdate,
    db: Session = Depends(get_db)
):
    document = db.query(models.Document).filter(
        models.Document.id == document_id
    ).first()

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    update_data = document_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(document, key, value)

    db.commit()
    db.refresh(document)

    return document

@app.delete(
    "/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = db.query(models.Document).filter(
        models.Document.id == document_id
    ).first()

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    db.delete(document)
    db.commit()

    return None

@app.post(
    "/auth/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    # Cek apakah username sudah digunakan
    existing_username = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Cek apakah email sudah digunakan
    existing_email = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password sebelum disimpan
    hashed_password = hash_password(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/auth/login", response_model=schemas.Token)
def login_user(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    # Cari user berdasarkan username
    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    # Verifikasi username dan password
    if not db_user or not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Buat JWT
    access_token = create_access_token(
        data={
            "sub": str(db_user.id),
            "role": db_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/auth/me", response_model=schemas.UserResponse)
def read_current_user(
    current_user: models.User = Depends(get_current_user)
):
    return current_user

@app.get("/user/dashboard")
def user_dashboard(
    current_user: models.User = Depends(
        require_role("user", "admin")
    )
):
    return {
        "message": "Welcome to User Dashboard",
        "username": current_user.username,
        "role": current_user.role
    }

@app.get("/admin/dashboard")
def admin_dashboard(
    current_user: models.User = Depends(
        require_role("admin")
    )
):
    return {
        "message": "Welcome to Admin Dashboard",
        "username": current_user.username,
        "role": current_user.role
    }