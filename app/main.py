import app
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.settings import settings
from app.routers import web_home, medicines, sales
from app import diag_backend

# app.include_router(diag_backend.router)

# Create tables only for SQLite
if settings.DB_BACKEND == "sqlite":
    from app.db.session_sqlite import engine
    from app.db.base import create_all
    create_all(engine)

app = FastAPI(title="Pharmacy Management System")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(web_home.router)
app.include_router(medicines.router)
app.include_router(sales.router)
