# backend/services/document_service.py
from sqlalchemy.orm import Session
from backend.models.document import Document
from backend.schemas.document import DocumentCreate, DocumentUpdate
from fastapi import HTTPException
from datetime import datetime


def upload_document(db: Session, data: DocumentCreate):
    new_doc = Document(
        name=data.name,
        file_path=data.file_path,
        uploaded_by=data.uploaded_by,
        project_id=data.project_id,
        version=1,
        uploaded_at=datetime.utcnow(),
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc


def update_document(db: Session, doc_id: int, data: DocumentUpdate):
    doc = db.query(Document).get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(doc, k, v)
    doc.version += 1
    db.commit()
    db.refresh(doc)
    return doc