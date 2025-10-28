# backend/api/endpoints/documents.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.db.session import get_db
from backend.models.document import Document  # assuming you have a Document model
from backend.schemas.document import DocumentCreate, DocumentRead  # Pydantic schemas

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

# --- Create a document ---
@router.post("/", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
def create_document(
    doc_in: DocumentCreate,
    db: Session = Depends(get_db)
):
    db_doc = Document(**doc_in.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

# --- Get all documents ---
@router.get("/", response_model=List[DocumentRead])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = db.query(Document).offset(skip).limit(limit).all()
    return documents

# --- Get a document by ID ---
@router.get("/{doc_id}", response_model=DocumentRead)
def read_document(doc_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return document

# --- Delete a document ---
@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    db.delete(document)
    db.commit()
    return None