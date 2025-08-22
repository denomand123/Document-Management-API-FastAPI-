from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from .config import get_settings
from .logging_config import setup_logging
from .auth import api_key_auth_middleware
from .routers import documents, search, users

setup_logging()
settings = get_settings()

app = FastAPI(
	title="Document Management API",
	description="REST API for managing and processing documents with embeddings",
	version="0.1.0",
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.middleware("http")(api_key_auth_middleware)

app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(users.router, prefix="/api/users", tags=["users"])


def custom_openapi():
	if app.openapi_schema:
		return app.openapi_schema
	openapi_schema = get_openapi(
		title=app.title,
		version=app.version,
		description=app.description,
		routes=app.routes,
	)
	openapi_schema["components"]["securitySchemes"] = {
		"ApiKeyAuth": {
			"type": "apiKey",
			"in": "header",
			"name": "x-api-key",
		}
	}
	openapi_schema["security"] = [{"ApiKeyAuth": []}]
	app.openapi_schema = openapi_schema
	return app.openapi_schema


app.openapi = custom_openapi 