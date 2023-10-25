from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "local_adocaosciente"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()