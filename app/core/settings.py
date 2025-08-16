import os
from dataclasses import dataclass

@dataclass
class Settings:
    DB_BACKEND: str = os.getenv("DB_BACKEND", "sqlite").lower()  # "sqlite" or "mongo"
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB: str = os.getenv("MONGO_DB", "pharmacy")

settings = Settings()
