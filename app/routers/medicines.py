from typing import Optional
from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import date
from fastapi.templating import Jinja2Templates
from app.models.medicine import Medicine
from app.reepositries.provider import get_medicines_repo


router = APIRouter(prefix="/medicines", tags=["medicines"])
templates = Jinja2Templates(directory="app/templates")

def _as_bool(v: Optional[str]) -> bool:
    return False if v is None else str(v).strip().lower() in ("1","true","on","yes")

@router.get("/", response_class=HTMLResponse)
async def list_page(
    request: Request,
    q: Optional[str] = None,
    manufacturer: Optional[str] = None,
    low: Optional[str] = Query(default=None),
    expired: Optional[str] = None,
    repo = Depends(get_medicines_repo),
):
    today = date.today()
    low_int = None
    if low and low.strip():
        try: low_int = int(low.strip())
        except ValueError: pass

    meds = repo.list(name=q, manufacturer=manufacturer, low=low_int, expired=_as_bool(expired), today=today)
    return templates.TemplateResponse("medicines/list.html", {"request": request, "medicines": meds, "today": today})

@router.get("/new", response_class=HTMLResponse)
async def new_form(request: Request):
    return templates.TemplateResponse("medicines/form.html", {"request": request, "medicine": None})

@router.post("/new")
async def create(
    name: str,
    manufacturer: Optional[str] = None,
    expiry_date: Optional[str] = None,
    price: float = 0,
    quantity: int = 0,
    repo = Depends(get_medicines_repo),
):
    exp = None
    if expiry_date:
        try: exp = date.fromisoformat(expiry_date)
        except ValueError: pass
    repo.create(Medicine(name=name.strip(), manufacturer=(manufacturer or None), expiry_date=exp, price=price, quantity=quantity))
    return RedirectResponse(url="/medicines/", status_code=303)

@router.get("/{id}/edit", response_class=HTMLResponse)
async def edit_form(id: int, request: Request, repo = Depends(get_medicines_repo)):
    m = repo.get(id)
    return templates.TemplateResponse("medicines/form.html", {"request": request, "medicine": m})

@router.post("/{id}/edit")
async def update(
    id: int,
    name: Optional[str] = None,
    manufacturer: Optional[str] = None,
    expiry_date: Optional[str] = None,
    price: Optional[float] = None,
    quantity: Optional[int] = None,
    repo = Depends(get_medicines_repo),
):
    data = {"name": name, "manufacturer": manufacturer, "price": price, "quantity": quantity}
    if expiry_date is not None:
        if expiry_date == "": data["expiry_date"] = None
        else:
            try: data["expiry_date"] = date.fromisoformat(expiry_date)
            except ValueError: pass
    repo.update(id, data)
    return RedirectResponse(url="/medicines/", status_code=303)

@router.post("/{id}/delete")
async def delete(id: int, repo = Depends(get_medicines_repo)):
    repo.delete(id)
    return RedirectResponse(url="/medicines/", status_code=303)
