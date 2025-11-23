from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Football Settings
    API_SPORTS_KEY: Optional[str] = Field(None, alias="API_SPORTS_KEY", description="x-apisports-key")
    API_SPORTS_HOST: str = Field("v3.football.api-sports.io", alias="API_SPORTS_HOST", description="x-apisports-host")
    API_SPORTS_BASE_URL: str = Field("https://v3.football.api-sports.io", alias="API_SPORTS_BASE_URL",
                                     description="Base URL for API-Football")

    PG_HOST: str = Field("localhost", alias="PG_HOST")
    PG_PORT: int = Field(5432, alias="PG_PORT")
    PG_USERNAME: str = Field("postgres", alias="PG_USERNAME")
    PG_PASSWORD: str = Field("postgres", alias="PG_PASSWORD")
    PG_DB_NAME: str = Field("postgres", alias="PG_DB_NAME")
    PG_DB_DRIVER: str = Field("postgresql", alias="PG_DB_DRIVER")

    INTERNAL_DATABASE_URL: Optional[str] = Field(None, alias="INTERNAL_DATABASE_URL")

    @property
    def postgres_url(self) -> str:
        """Асинхронне посилання для SQLAlchemy (app)"""
        if self.INTERNAL_DATABASE_URL:
            # Якщо Render надав internal URL, додаємо asyncpg драйвер якщо його немає
            if "asyncpg" not in self.INTERNAL_DATABASE_URL:
                return self.INTERNAL_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
            return self.INTERNAL_DATABASE_URL

        return (
            f"{self.PG_DB_DRIVER}+asyncpg://{self.PG_USERNAME}:{self.PG_PASSWORD}@"
            f"{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB_NAME}"
        )

    @property
    def postgres_url_sync(self) -> str:
        """Синхронне посилання для Alembic migrations"""
        if self.INTERNAL_DATABASE_URL:
            return self.INTERNAL_DATABASE_URL

        return (
            f"{self.PG_DB_DRIVER}://{self.PG_USERNAME}:{self.PG_PASSWORD}@"
            f"{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB_NAME}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


settings = Settings()