from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
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

    REDIS_HOST: str = Field("localhost", alias="REDIS_HOST")
    REDIS_PORT: int = Field(6379, alias="REDIS_PORT")
    REDIS_TTL: int = Field(3600, alias="REDIS_TTL", description="Cache TTL in seconds (default 1 hour)")

    REDIS_URL_ENV: Optional[str] = Field(None, alias="REDIS_URL")

    @property
    def redis_url(self) -> str:
        if self.REDIS_URL_ENV:
            return self.REDIS_URL_ENV
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def postgres_url(self) -> str:
        if self.INTERNAL_DATABASE_URL:
            if "asyncpg" not in self.INTERNAL_DATABASE_URL:
                return self.INTERNAL_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
            return self.INTERNAL_DATABASE_URL
        return f"{self.PG_DB_DRIVER}+asyncpg://{self.PG_USERNAME}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB_NAME}"

    @property
    def postgres_url_sync(self) -> str:
        if self.INTERNAL_DATABASE_URL:
            return self.INTERNAL_DATABASE_URL
        return f"{self.PG_DB_DRIVER}://{self.PG_USERNAME}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


settings = Settings()