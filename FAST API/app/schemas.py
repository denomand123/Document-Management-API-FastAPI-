from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class UserCreate(BaseModel):
	email: str
	name: Optional[str] = None


class DocumentCreate(BaseModel):
	title: str
	text: str
	owner_id: Optional[int] = None


class DocumentRead(BaseModel):
	id: int
	title: str
	content_text: str
	owner_id: Optional[int]
	created_at: datetime
	class Config:
		from_attributes = True


class ChunkRead(BaseModel):
	id: int
	document_id: int
	chunk_index: int
	text: str
	created_at: datetime
	class Config:
		from_attributes = True


class SearchQuery(BaseModel):
	query: str
	top_k: int = 5 