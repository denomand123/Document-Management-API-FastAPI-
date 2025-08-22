"""In-memory embeddings store and simple similarity search.

- Embedding: naive bag-of-words hashed into a fixed-size vector (demo only)
- Cosine similarity via dot product of L2-normalized vectors
- Store keyed by (document_id, chunk_index) with original text for reference
"""
from __future__ import annotations
from typing import Dict, List, Tuple
import math
import hashlib


def _text_to_embedding(text: str, dim: int = 128) -> List[float]:
	vec = [0.0] * dim
	for token in text.split():
		h = int(hashlib.sha256(token.encode("utf-8")).hexdigest(), 16)
		idx = h % dim
		vec[idx] += 1.0
	norm = math.sqrt(sum(v * v for v in vec)) or 1.0
	return [v / norm for v in vec]


def cosine_similarity(a: List[float], b: List[float]) -> float:
	dot = sum(x * y for x, y in zip(a, b))
	return dot


class InMemoryEmbeddingsStore:
	def __init__(self, dim: int = 128) -> None:
		self.dim = dim
		self._vectors: Dict[Tuple[str, int], List[float]] = {}
		self._texts: Dict[Tuple[str, int], str] = {}

	def add(self, doc_key: str, chunk_index: int, text: str) -> None:
		emb = _text_to_embedding(text, self.dim)
		key = (doc_key, chunk_index)
		self._vectors[key] = emb
		self._texts[key] = text

	def delete_document(self, doc_key: str) -> None:
		for key in list(self._vectors.keys()):
			if key[0] == doc_key:
				self._vectors.pop(key, None)
				self._texts.pop(key, None)

	def search(self, query: str, top_k: int = 5) -> List[Tuple[Tuple[str, int], float, str]]:
		q_emb = _text_to_embedding(query, self.dim)
		scores: List[Tuple[Tuple[str, int], float, str]] = []
		for key, emb in self._vectors.items():
			s = cosine_similarity(q_emb, emb)
			scores.append((key, s, self._texts[key]))
		scores.sort(key=lambda x: x[1], reverse=True)
		return scores[:top_k] 