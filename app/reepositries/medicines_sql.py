from typing import Iterable, Optional, List
from datetime import date
from sqlmodel import select
from sqlalchemy import func
from app.models.medicine import Medicine

class MedicinesRepoSQL:
    def __init__(self, session):
        self.session = session

    def create(self, m: Medicine) -> Medicine:
        self.session.add(m)
        self.session.commit()
        self.session.refresh(m)
        return m

    def get(self, id: int) -> Optional[Medicine]:
        return self.session.get(Medicine, id)

    def list(
        self,
        *,
        name: Optional[str] = None,
        manufacturer: Optional[str] = None,
        low: Optional[int] = None,
        expired: bool = False,
        today: Optional[date] = None,
    ) -> Iterable[Medicine]:
        stmt = select(Medicine)

        if name:
            term = f"%{name.strip().lower()}%"
            stmt = stmt.where(func.lower(Medicine.name).like(term))

        if manufacturer:
            term = f"%{manufacturer.strip().lower()}%"
            stmt = stmt.where(func.lower(func.coalesce(Medicine.manufacturer, "")).like(term))

        if expired:
            cutoff = today or date.today()
            stmt = stmt.where(Medicine.expiry_date.is_not(None)).where(func.date(Medicine.expiry_date) < cutoff)

        if low is not None:
            stmt = stmt.where(Medicine.quantity < low)

        return list(self.session.exec(stmt))

    def update(self, id: int, data: dict) -> Medicine:
        m = self.session.get(Medicine, id)
        if not m:
            raise ValueError("Medicine not found")
        for k, v in data.items():
            if v is not None:
                setattr(m, k, v)
        self.session.add(m)
        self.session.commit()
        self.session.refresh(m)
        return m

    def delete(self, id: int) -> None:
        m = self.session.get(Medicine, id)
        if m:
            self.session.delete(m)
            self.session.commit()

    def expired(self, today: date) -> List[Medicine]:
        stmt = select(Medicine).where(Medicine.expiry_date.is_not(None)).where(func.date(Medicine.expiry_date) < today)
        return list(self.session.exec(stmt))

    def low_stock(self, threshold: int) -> List[Medicine]:
        stmt = select(Medicine).where(Medicine.quantity < threshold)
        return list(self.session.exec(stmt))
