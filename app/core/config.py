from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    CLERK_FRONTEND_API : Optional[str] = None
    BACKEND_API_CLERK_URL: Optional[str] = None
    CLERK_SECRET_KEY: Optional[str] = None
    CLERK_JWKS_URL :str = ""

    @property
    def DATABASE_URL(self) -> str:
        if not (self.POSTGRES_USER and self.POSTGRES_PASSWORD and self.POSTGRES_DB):
            raise ValueError("POSTGRES_USER, POSTGRES_PASSWORD and POSTGRES_DB must be set")
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def DATABASE_URL_SYNC(self) -> str:
        if not (self.POSTGRES_USER and self.POSTGRES_PASSWORD and self.POSTGRES_DB):
            raise ValueError(
                "POSTGRES_USER, POSTGRES_PASSWORD and POSTGRES_DB must be set"
            )

        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    class Config:
        env_file = ".env"
        case_sensitive = True



@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
