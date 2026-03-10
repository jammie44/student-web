from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./studenthub.db"

    # Redis - using in-memory for Python only
    redis_url: str = "memory://"

    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    max_tokens: int = 4000

    # JWT
    secret_key: str = "your_secret_key_here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Stripe
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_webhook_secret: str = ""

    # Application
    app_name: str = "StudentHub"
    app_version: str = "1.0.0"
    debug: bool = True

    # Vector Store
    faiss_index_path: str = "./vector_store/faiss_index"

    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60

    # Celery - using in-memory
    celery_broker_url: str = "memory://"
    celery_result_backend: str = "memory://"

    class Config:
        env_file = ".env"


settings = Settings()