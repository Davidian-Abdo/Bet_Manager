# backend/schemas/document.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentBase(BaseModel):
    name: str
    file_path: str
    project_id: int


class DocumentCreate(DocumentBase):
    uploaded_by: int


class DocumentUpdate(BaseModel):
    name: Optional[str]
    version: Optional[int]


class DocumentOut(DocumentBase):
    id: int
    uploaded_by: int
    version: int
    uploaded_at: datetime

    class Config:
        orm_mode = True