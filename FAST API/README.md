# Document Management API (FastAPI)

## Setup

1. Create a virtual environment
```bash
python -m venv .venv
. .venv/Scripts/Activate.ps1
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure environment
```bash
set DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/fastapi_docs
set API_KEY=changeme
```

4. Create database tables
```bash
psql "%DATABASE_URL%" -f migrations/001_init.sql
```

5. Run the API
```bash
uvicorn app.main:app --reload
```

- Docs: http://localhost:8000/docs

## API Endpoints

- `POST /api/users/` - Create user
- `POST /api/documents/` - Create document from text
- `POST /api/documents/upload` - Upload text file
- `POST /api/documents/ingest-external/{id}` - Ingest from mock external system
- `GET /api/documents/` - List documents
- `DELETE /api/documents/{id}` - Delete document
- `POST /api/search/similar` - Semantic search

## Notes
- Uses PostgreSQL for storage and a simple in-memory embeddings index.
- API key auth via `x-api-key` header. 