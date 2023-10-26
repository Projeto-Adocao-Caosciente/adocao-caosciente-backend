import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()