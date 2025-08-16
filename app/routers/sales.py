from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session
from fastapi.templating import Jinja2Templates
from datetime import datetime

from app.db.session_sqlite import get_session
from app.reepositries.sales_sql import SalesRepoSQL
from app.reepositries.medicines_sql import MedicinesRepoSQL
from app.models.sale import Sale
from app.services.revenue import compute_total
from app.reepositries.provider import get_sales_repo, get_medicines_repo

router = APIRouter(prefix="/sales", tags=["sales"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def list_page(request: Request, session: Session = Depends(get_session)):
    sales = SalesRepoSQL(session).list()
    return templates.TemplateResponse("sales/list.html", {"request": request, "sales": sales})

@router.get("/new", response_class=HTMLResponse)
async def new_form(request: Request, session: Session = Depends(get_session)):
    meds = MedicinesRepoSQL(session).list()
    return templates.TemplateResponse("sales/form.html", {"request": request, "medicines": meds})

@router.post("/new")
async def create(
    medicine_id: int = Form(...),
    quantity: int = Form(...),
    unit_price: float = Form(...),
    session: Session = Depends(get_session),
):
    total = compute_total(quantity, unit_price)
    sale = Sale(medicine_id=medicine_id, quantity=quantity, unit_price=unit_price, total=total, created_at=datetime.utcnow())
    SalesRepoSQL(session).create(sale)

    # decrement inventory
    meds_repo = MedicinesRepoSQL(session)
    m = meds_repo.get(medicine_id)
    if m:
        new_qty = max(0, (m.quantity or 0) - quantity)
        meds_repo.update(medicine_id, {"quantity": new_qty})

    return RedirectResponse(url="/sales/", status_code=303)

@router.get("/revenue", response_class=HTMLResponse)
async def revenue_page(request: Request, session: Session = Depends(get_session)):
    sales_repo = SalesRepoSQL(session)
    daily = sales_repo.revenue_daily()
    monthly = sales_repo.revenue_monthly()
    return templates.TemplateResponse("sales/revenue.html", {"request": request, "daily": daily, "monthly": monthly})
