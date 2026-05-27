from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "NNgo API"
    debug: bool = False

    database_url: str = Field(
        default="mysql+asyncmy://nngo:nngo_secret@localhost:3306/nngo_db?charset=utf8mb4",
        description="Async SQLAlchemy URL (asyncmy driver)",
    )

    redis_url: str = "redis://localhost:6379/0"

    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_recycle: int = 3600

    jwt_secret_key: str = Field(
        default="change-me-in-production-use-openssl-rand-hex-32",
        description="HS256 signing secret",
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14


@lru_cache
def get_settings() -> Settings:
    return Settings()
