from app.database import engine, Base
from app import models

# Membuat seluruh tabel berdasarkan model
Base.metadata.create_all(bind=engine)

print("Tabel database berhasil dibuat!")