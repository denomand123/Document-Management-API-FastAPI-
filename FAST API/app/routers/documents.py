"""Documents router.

- POST /api/documents/ : create from raw text (stores doc + chunks + embeddings)
- POST /api/documents/upload : upload a text file (UTF-8 assumed)
- POST /api/documents/ingest-external/{id} : fetch from mock external system
- GET /api/documents/ : list documents
- DELETE /api/documents/{id} : delete document and its embeddings
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models
from ..schemas import DocumentCreate, DocumentRead, ChunkRead
from ..services.processing import extract_text_from_bytes, chunk_text
from ..state import embeddings_store
from ..services.mock_docs import fetch_document_text

router = APIRouter()

_embeddings = embeddings_store


@router.post("/", response_model=DocumentRead)
def create_document(payload: DocumentCreate, db: Session = Depends(get_db)):
	text = payload.text
	if not text:
		raise HTTPException(status_code=400, detail="Empty text")
	doc = models.Document(title=payload.title, content_text=text, owner_id=payload.owner_id)
	db.add(doc)
	db.commit()
	db.refresh(doc)
	chunks = chunk_text(text)
	for idx, ch in enumerate(chunks):
		chunk = models.DocumentChunk(document_id=doc.id, chunk_index=idx, text=ch)
		db.add(chunk)
		db.flush()
		_embeddings.add(str(doc.id), idx, ch)
	db.commit()
	return doc


@router.post("/upload", response_model=DocumentRead)
async def upload_document(
	file: UploadFile = File(...),
	title: str = Form(...),
	owner_id: int | None = Form(None),
	db: Session = Depends(get_db),
):
	data = await file.read()
	text = extract_text_from_bytes(data, file.filename)
	if not text:
		raise HTTPException(status_code=400, detail="Unsupported or empty file")
	doc = models.Document(title=title, content_text=text, owner_id=owner_id)
	db.add(doc)
	db.commit()
	db.refresh(doc)
	chunks = chunk_text(text)
	for idx, ch in enumerate(chunks):
		chunk = models.DocumentChunk(document_id=doc.id, chunk_index=idx, text=ch)
		db.add(chunk)
		db.flush()
		_embeddings.add(str(doc.id), idx, ch)
	db.commit()
	return doc


@router.post("/ingest-external/{external_id}", response_model=DocumentRead)
def ingest_from_mock(external_id: str, db: Session = Depends(get_db)):
	text = fetch_document_text(external_id)
	if not text:
		raise HTTPException(status_code=404, detail="External document not found")
	doc = models.Document(title=f"External {external_id}", content_text=text)
	db.add(doc)
	db.commit()
	db.refresh(doc)
	chunks = chunk_text(text)
	for idx, ch in enumerate(chunks):
		chunk = models.DocumentChunk(document_id=doc.id, chunk_index=idx, text=ch)
		db.add(chunk)
		db.flush()
		_embeddings.add(str(doc.id), idx, ch)
	db.commit()
	return doc


@router.get("/", response_model=List[DocumentRead])
def list_documents(db: Session = Depends(get_db)):
	return db.query(models.Document).order_by(models.Document.id.desc()).all()


@router.delete("/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
	doc = db.get(models.Document, doc_id)
	if not doc:
		raise HTTPException(status_code=404, detail="Document not found")
	_embeddings.delete_document(str(doc.id))
	db.delete(doc)
	db.commit()
	return {"deleted": True} 