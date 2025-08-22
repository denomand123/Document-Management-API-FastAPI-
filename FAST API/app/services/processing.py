from typing import List
from ..config import get_settings


def extract_text_from_bytes(data: bytes, filename: str | None = None) -> str:
	try:
		return data.decode("utf-8")
	except Exception:
		return ""


def chunk_text(text: str) -> List[str]:
	settings = get_settings()
	size = max(50, settings.chunk_size)
	overlap = max(0, min(settings.overlap, size - 1))
	chunks: List[str] = []
	start = 0
	while start < len(text):
		end = min(start + size, len(text))
		chunks.append(text[start:end])
		if end == len(text):
			break
		start = end - overlap
	return chunks 