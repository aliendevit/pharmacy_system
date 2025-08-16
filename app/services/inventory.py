# app/services/inventory.py
from app.models.medicine import Medicine

def compute_low_stock(medicines, threshold: int = 10):
    return [m for m in medicines if (m.quantity or 0) < threshold]