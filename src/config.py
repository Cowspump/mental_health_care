"""
config.py (ИСПРАВЛЕНО)
"""
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    # 1. Database settings (с префиксом 'database_' для Pydantic)
    database_url: str = Field(
        default="sqlite+aiosqlite:///./mental_health.db",
        description="Database connection URL"
    )

    # 2. Security settings
    secret_key: str = Field(
        ...,  # Required field
        description="Secret key for JWT token generation"
    )
    algorithm: str = Field(
        default="HS256",
        description="JWT algorithm"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="JWT token expiration time in minutes"
    )

    # 3. API settings
    api_v1_str: str = Field(
        default="/api/v1",
        description="API version 1 prefix"
    )
    project_name: str = Field(
        default="Mental Health Platform",
        description="Project name for OpenAPI docs"
    )
    debug: bool = Field(
        default=False,
        description="Debug mode flag"
    )

    # Конфигурация Pydantic Settings
    model_config = SettingsConfigDict(
        # Убедитесь, что .env файл находится в /mental_health_care/.env
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Pydantic будет искать SECRET_KEY, несмотря на то что в коде secret_key
    )


# Global settings instance
settings = Settings()