from pathlib import Path
from typing import List

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = "development"
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REDIS_URL: str = "redis://redis:6379/0"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    STATIC_DIR: str = str(Path(__file__).resolve().parent.parent / "static")
    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str | None = None
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    RATE_LIMIT_LOGIN: int = 8
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors(cls, v):
        if isinstance(v, str):
            import json

            try:
                return json.loads(v)
            except Exception:
                return [item.strip() for item in v.split(",") if item.strip()]
        return v

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def is_production(self) -> bool:
        return self.ENV.lower() in {"prod", "production"}


settings = Settings()
