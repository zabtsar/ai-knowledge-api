from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

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