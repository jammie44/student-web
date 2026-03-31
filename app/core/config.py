from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    app_name: str = "StudyHub"
    app_version: str = "2.0.0"
    debug: bool = False

    database_url: str = "sqlite:///./studyhub.db"
    secret_key: str = "change-me-to-a-long-random-secret-key-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 days — persistent login

    frontend_url: str = "*"
    huggingface_api_key: str = ""

    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""

    @property
    def pg_database_url(self) -> str:
        url = self.database_url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url


settings = Settings()
