from sqlalchemy import text
from app.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        version = result.fetchone()

        print("Koneksi PostgreSQL berhasil!")
        print(f"Database version: {version[0]}")

except Exception as e:
    print("Koneksi PostgreSQL gagal!")
    print(f"Error: {e}")