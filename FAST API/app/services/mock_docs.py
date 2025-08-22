"""Mock external document system.

- Simulates fetching an external document by ID
- Used by /api/documents/ingest-external/{id}
"""
from typing import Optional


MOCK_DOCS = {
	"doc-001": "This is a sample external document about FastAPI and testing.",
	"doc-002": "Another document describes embeddings and similarity search.",
}


def fetch_document_text(doc_id: str) -> Optional[str]:
	return MOCK_DOCS.get(doc_id) 