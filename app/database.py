import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Membaca konfigurasi dari file .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Membuat koneksi ke PostgreSQL
engine = create_engine(DATABASE_URL)

# Membuat session database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base untuk model database
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()