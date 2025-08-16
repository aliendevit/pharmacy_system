# app/routers/diag_backend.py
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from app.core.settings import settings

router = APIRouter(prefix="/_diag", tags=["diag"])

@router.get("/backend", response_class=PlainTextResponse)
def which_backend():
    return f"DB_BACKEND={settings.DB_BACKEND}"
