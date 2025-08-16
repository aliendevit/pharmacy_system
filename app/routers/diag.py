from datetime import datetime, date
from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlmodel import Session
from app.db.session_sqlite import get_session
from app.reepositries.medicines_sql import MedicinesRepoSQL

router = APIRouter(prefix="/_diag", tags=["diag"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/ping", response_class=PlainTextResponse)
def ping():
    # proves the ASGI app is running and returning immediately
    return "pong"

@router.get("/time", response_class=PlainTextResponse)
def time():
    # quick dynamic response
    return datetime.utcnow().isoformat() + "Z"

@router.get("/medicines.json", response_class=JSONResponse)
def meds_json(session: Session = Depends(get_session)):
    # bypass Jinja to isolate DB
    repo = MedicinesRepoSQL(session)
    meds = repo.list()
    return JSONResponse([
        {
            "id": m.id,
            "name": m.name,
            "manufacturer": m.manufacturer,
            "expiry_date": m.expiry_date.isoformat() if m.expiry_date else None,
            "price": m.price,
            "quantity": m.quantity,
        }
        for m in meds
    ])

@router.get("/template", response_class=HTMLResponse)
def minimal_template(request: Request):
    # minimal Jinja render (no CSS/JS)
    return templates.TemplateResponse("diag/minimal.html", {"request": request, "today": date.today()})
