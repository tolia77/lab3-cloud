# ...existing code...
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_SPORTS_KEY: Optional[str] = Field(alias="API_SPORTS_KEY", description="x-apisports-key")
    API_SPORTS_HOST: str = Field("v3.football.api-sports.io", alias="API_SPORTS_HOST", description="x-apisports-host")
    API_SPORTS_BASE_URL: str = Field("https://v3.football.api-sports.io",  alias="API_SPORTS_BASE_URL", description="Base URL for API-Football")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()