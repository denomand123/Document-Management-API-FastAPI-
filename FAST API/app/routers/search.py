from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models
from ..schemas import SearchQuery, ChunkRead
from ..state import embeddings_store

router = APIRouter()

_embeddings = embeddings_store


@router.post("/similar", response_model=List[ChunkRead])
def semantic_search(payload: SearchQuery, db: Session = Depends(get_db)):
	if not payload.query:
		raise HTTPException(status_code=400, detail="Empty query")
	results = _embeddings.search(payload.query, top_k=payload.top_k)
	chunks: List[models.DocumentChunk] = []
	for (doc_key, chunk_index), score, text in results:
		try:
			doc_id = int(doc_key)
		except ValueError:
			continue
		chunk = (
			db.query(models.DocumentChunk)
			.filter(models.DocumentChunk.document_id == doc_id, models.DocumentChunk.chunk_index == chunk_index)
			.first()
		)
		if chunk:
			chunks.append(chunk)
	return chunks 