from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "StudyHub"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database — Render injects DATABASE_URL automatically
    database_url: str = "sqlite:///./studyhub.db"

    # JWT
    secret_key: str = "changeme-please-set-a-real-secret-key-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 days

    # CORS
    frontend_url: str = "*"

    # Stripe (optional)
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def pg_database_url(self) -> str:
        """Render gives postgres:// but SQLAlchemy needs postgresql://"""
        url = self.database_url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url


settings = Settings()
