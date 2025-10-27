from pydantic import BaseSettings, Field, SecretStr


class Settings(BaseSettings):
    external_api_key: SecretStr = Field(alias="EXTERNAL_API_KEY")
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# singleton instance to import from other modules:
settings = Settings()

