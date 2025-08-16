from typing import Generator
from fastapi import HTTPException
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from app.core.settings import settings

# Short timeout so UI doesn't "spin" forever when Mongo isn't reachable
_client = MongoClient(
    settings.MONGO_URI,
    serverSelectionTimeoutMS=2000,  # 2 seconds
)
_db = _client[settings.MONGO_DB]

def get_db() -> Generator:
    """
    FastAPI dependency that yields a PyMongo Database.
    Pings first so we fail fast if Mongo isn't available.
    """
    try:
        _client.admin.command("ping")
    except ServerSelectionTimeoutError as e:
        raise HTTPException(status_code=503, detail=f"MongoDB unavailable: {str(e)}")
    yield _db
