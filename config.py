# config.py
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    SECRET_KEY: str = "dev_secret_key"
    WEATHER_API_KEY: str = "your_openweather_api_key_here"
    DATABASE_URL: str = str(BASE_DIR / "instance" / "quiz.db")
    DEBUG: bool = True

    QUIZ_SAMPLE_PATH: str = str(BASE_DIR / "instance" / "quiz.jsonl")

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
