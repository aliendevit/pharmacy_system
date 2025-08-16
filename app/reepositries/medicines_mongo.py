from typing import Iterable, Optional, List, Dict, Any
from datetime import date
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import ReturnDocument
from app.models.medicine import Medicine
import re

def _to_iso(d: Optional[date]) -> Optional[str]:
    return d.isoformat() if d else None

def _from_iso(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    return date.fromisoformat(s)

def _to_model(doc: Dict[str, Any]) -> Medicine:
    return Medicine(
        id=int(doc["id"]),
        name=doc["name"],
        manufacturer=doc.get("manufacturer"),
        expiry_date=_from_iso(doc.get("expiry_date")),
        price=float(doc.get("price", 0.0)),
        quantity=int(doc.get("quantity", 0)),
    )

class MedicinesRepoMongo:
    """
    Mongo-backed repo that keeps integer ids via a counters collection.
    Collection: 'medicines'
      { id: int, name: str, manufacturer: str|None, expiry_date: 'YYYY-MM-DD'|None, price: float, quantity: int }
    """
    def __init__(self, db: Database):
        self.db: Database = db
        self.col: Collection = db["medicines"]
        self.counters: Collection = db["counters"]
        self.col.create_index("id", unique=True)
        self.col.create_index("name")
        self.col.create_index("manufacturer")

    def _next_id(self, key: str = "medicines") -> int:
        doc = self.counters.find_one_and_update(
            {"_id": key},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return int(doc.get("seq", 1))

    def create(self, m: Medicine) -> Medicine:
        new_id = self._next_id()
        doc = {
            "id": new_id,
            "name": m.name,
            "manufacturer": m.manufacturer,
            "expiry_date": _to_iso(m.expiry_date),
            "price": float(m.price or 0.0),
            "quantity": int(m.quantity or 0),
        }
        self.col.insert_one(doc)
        return self.get(new_id)

    def get(self, id: int) -> Optional[Medicine]:
        doc = self.col.find_one({"id": int(id)})
        return _to_model(doc) if doc else None

    def list(
        self,
        *,
        name: Optional[str] = None,
        manufacturer: Optional[str] = None,
        low: Optional[int] = None,
        expired: bool = False,
        today: Optional[date] = None,
    ) -> Iterable[Medicine]:
        q: Dict[str, Any] = {}

        if name:
            q["name"] = {"$regex": re.escape(name.strip()), "$options": "i"}

        if manufacturer:
            q["manufacturer"] = {"$regex": re.escape(manufacturer.strip()), "$options": "i"}

        if expired:
            cutoff = (today or date.today()).isoformat()
            q["expiry_date"] = {"$lt": cutoff, "$ne": None}

        if low is not None:
            q["quantity"] = {"$lt": int(low)}

        docs = list(self.col.find(q).sort("name", 1))
        return [_to_model(d) for d in docs]

    def update(self, id: int, data: dict) -> Medicine:
        patch: Dict[str, Any] = {}
        for k, v in data.items():
            if k == "expiry_date":
                if v is None:
                    # explicit remove of expiry
                    self.col.update_one({"id": int(id)}, {"$unset": {"expiry_date": ""}})
                    continue
                if isinstance(v, date):
                    patch["expiry_date"] = _to_iso(v)
                else:
                    patch["expiry_date"] = v
            elif v is not None:
                patch[k] = v

        if patch:
            self.col.update_one({"id": int(id)}, {"$set": patch})

        m = self.get(id)
        if not m:
            raise ValueError("Medicine not found")
        return m

    def delete(self, id: int) -> None:
        self.col.delete_one({"id": int(id)})

    def expired(self, today: date) -> List[Medicine]:
        return list(self.list(expired=True, today=today))

    def low_stock(self, threshold: int) -> List[Medicine]:
        return list(self.list(low=threshold))
