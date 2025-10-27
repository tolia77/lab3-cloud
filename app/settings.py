# ...existing code...
from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    API_SPORTS_KEY: Optional[str] = Field(None, description="x-apisports-key")
    API_SPORTS_HOST: str = Field("v3.football.api-sports.io", description="x-apisports-host")
    API_SPORTS_BASE_URL: str = Field("https://v3.football.api-sports.io", description="Base URL for API-Football")

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()