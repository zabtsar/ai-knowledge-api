from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from pydantic import Field


# Schema untuk membuat Document
class DocumentCreate(BaseModel):
    title: str
    content: Optional[str] = None
    user_id: Optional[int] = None

# Schema untuk memperbarui Document
class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# Schema untuk menampilkan Document
class DocumentResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    user_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str