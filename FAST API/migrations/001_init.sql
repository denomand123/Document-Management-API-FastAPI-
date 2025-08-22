-- Users table
CREATE TABLE IF NOT EXISTS users (
	id SERIAL PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255),
	created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
	id SERIAL PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	content_text TEXT NOT NULL,
	owner_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
	created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_documents_owner_id ON documents(owner_id);

-- Document chunks table
CREATE TABLE IF NOT EXISTS document_chunks (
	id SERIAL PRIMARY KEY,
	document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
	chunk_index INTEGER NOT NULL,
	text TEXT NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_document_chunks_document_id ON document_chunks(document_id);
CREATE UNIQUE INDEX IF NOT EXISTS ux_document_chunks_doc_idx ON document_chunks(document_id, chunk_index); 