"""Configuration (pydantic-settings)."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/polymarket_advisor"
    log_level: str = "INFO"
    polymarket_gamma_base_url: str = "https://gamma-api.polymarket.com"


@lru_cache
def get_settings() -> Settings:
    return Settings()
