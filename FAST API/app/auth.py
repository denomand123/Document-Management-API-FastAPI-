from fastapi import Request
from fastapi.responses import JSONResponse
from typing import Callable

from .config import get_settings


EXCLUDED_PATHS = {
	"/docs",
	"/openapi.json",
	"/redoc",
}


async def api_key_auth_middleware(request: Request, call_next: Callable):
	path = request.url.path
	if any(path == p or path.startswith(p + "/") for p in EXCLUDED_PATHS):
		return await call_next(request)
	settings = get_settings()
	api_key = request.headers.get("x-api-key")
	if not api_key or api_key != settings.api_key:
		return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
	response = await call_next(request)
	return response 