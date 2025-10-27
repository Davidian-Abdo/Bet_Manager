# backend/core/config.py
from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # --- App Metadata ---
    APP_NAME: str = "BET Manager"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    # --- Database ---
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str

    # --- Security ---
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  # 8 hours

    # --- Storage (S3 / MinIO) ---
    S3_ENDPOINT: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET: str

    # --- Realtime / Redis ---
    REDIS_URL: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()