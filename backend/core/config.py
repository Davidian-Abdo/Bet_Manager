from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional, List


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

    # --- Computed Database URL (ADD THIS) ---
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

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

     # CORS Configuration - ADD YOUR NGROK URL
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:8501",           # Streamlit local
        "http://127.0.0.1:8501",           # Streamlit local alternative  
        "https://camden-strangulative-freezingly.ngrok-free.dev",  # Your Ngrok URL
        # Add your Streamlit cloud URL when you deploy
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True  # Add this for consistency


# Simplify the settings instance (REMOVE LRU_CACHE for migrations)
settings = Settings()