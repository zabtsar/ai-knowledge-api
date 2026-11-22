from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship

from app.database import Base

# Model User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    # Relasi satu User memiliki banyak Document
    documents = relationship("Document", back_populates="user")

# Model Document
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relasi ke User
    user = relationship("User", back_populates="documents")