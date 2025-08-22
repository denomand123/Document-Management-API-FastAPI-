from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .db import Base


class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	email = Column(String(255), unique=True, nullable=False, index=True)
	name = Column(String(255), nullable=True)
	created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
	documents = relationship("Document", back_populates="owner")


class Document(Base):
	__tablename__ = "documents"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String(255), nullable=False)
	content_text = Column(Text, nullable=False)
	owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
	created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
	owner = relationship("User", back_populates="documents")
	chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
	__tablename__ = "document_chunks"
	id = Column(Integer, primary_key=True, index=True)
	document_id = Column(Integer, ForeignKey("documents.id"), nullable=False, index=True)
	chunk_index = Column(Integer, nullable=False)
	text = Column(Text, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
	document = relationship("Document", back_populates="chunks") 