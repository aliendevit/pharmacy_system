# app/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_BACKEND: str = "sqlite"  # or "mongo"
    LOW_STOCK_THRESHOLD: int = 10

settings = Settings()