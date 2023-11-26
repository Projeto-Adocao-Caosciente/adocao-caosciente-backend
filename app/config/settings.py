import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    DATABASE_URL_TEST: str = os.getenv("DATABASE_URL_TEST")
    DATABASE_NAME_TEST: str = os.getenv("DATABASE_NAME_TEST")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()