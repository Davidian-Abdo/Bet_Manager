# backend/models/document.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, JSON
from sqlalchemy.sql import func
from backend.db.base import Base
import enum

class DocumentType(str, enum.Enum):
    dwg = "dwg"
    pdf = "pdf"
    excel = "excel"
    report = "report"


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    doc_type = Column(Enum(DocumentType))
    file_url = Column(String(500), nullable=False)
    meta = Column(JSON)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())