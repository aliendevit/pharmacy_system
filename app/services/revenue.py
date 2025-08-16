# app/services/revenue.py
from app.models.sale import Sale

def compute_total(quantity: int, unit_price: float) -> float:
    return round(quantity * unit_price, 2)