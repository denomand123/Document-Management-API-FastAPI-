"""Application configuration using Pydantic Settings (v2).

- Reads environment variables (e.g., DATABASE_URL, API_KEY)
- Provides defaults for local development
- Use a .env file or set env vars in your shell
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	app_env: str = "dev"
	database_url: str = "postgresql+psycopg2://user:password@localhost:5432/fastapi_docs"
	api_key: str = "changeme"
	chunk_size: int = 500
	overlap: int = 50
	model_config = SettingsConfigDict(env_file=".env", env_prefix="", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
	return Settings() 