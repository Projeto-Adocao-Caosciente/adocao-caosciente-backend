import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "None")
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "None")
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME", "None")
    DATABASE_URL_TEST: str = os.environ.get("DATABASE_URL_TEST", "None")
    DATABASE_NAME_TEST: str = os.environ.get("DATABASE_NAME_TEST", "None")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()