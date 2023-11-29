import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "")
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "")
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME", "")
    DATABASE_URL_TEST: str = os.environ.get("DATABASE_URL_TEST", "")
    DATABASE_NAME_TEST: str = os.environ.get("DATABASE_NAME_TEST", "")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()