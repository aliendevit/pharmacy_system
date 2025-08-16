from typing import Iterable, Optional, List, Tuple, Dict, Any
from datetime import datetime
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import ReturnDocument
from app.models.sale import Sale

def _to_model(doc: Dict[str, Any]) -> Sale:
    return Sale(
        id=int(doc["id"]),
        medicine_id=int(doc["medicine_id"]),
        quantity=int(doc["quantity"]),
        unit_price=float(doc["unit_price"]),
        total=float(doc["total"]),
        created_at=doc["created_at"],
    )

class SalesRepoMongo:
    """
    Mongo-backed sales with integer ids and simple aggregations.
    Collection: 'sales'
      { id: int, medicine_id: int, quantity: int, unit_price: float, total: float, created_at: datetime }
    """
    def __init__(self, db: Database):
        self.db: Database = db
        self.col: Collection = db["sales"]
        self.counters: Collection = db["counters"]
        self.col.create_index("id", unique=True)
        self.col.create_index("created_at")

    def _next_id(self, key: str = "sales") -> int:
        doc = self.counters.find_one_and_update(
            {"_id": key},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return int(doc.get("seq", 1))

    def create(self, s: Sale) -> Sale:
        new_id = self._next_id()
        doc = {
            "id": new_id,
            "medicine_id": int(s.medicine_id),
            "quantity": int(s.quantity),
            "unit_price": float(s.unit_price),
            "total": float(s.total),
            "created_at": s.created_at or datetime.utcnow(),
        }
        self.col.insert_one(doc)
        return self.get(new_id)

    def list(self, *, since: Optional[datetime] = None, until: Optional[datetime] = None) -> Iterable[Sale]:
        q: Dict[str, Any] = {}
        if since:
            q["created_at"] = q.get("created_at", {})
            q["created_at"]["$gte"] = since
        if until:
            q["created_at"] = q.get("created_at", {})
            q["created_at"]["$lt"] = until
        docs = list(self.col.find(q).sort("created_at", -1))
        return [_to_model(d) for d in docs]

    def revenue_daily(self) -> List[Tuple[str, float]]:
        pipeline = [
            {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}}, "revenue": {"$sum": "$total"}}},
            {"$sort": {"_id": -1}},
        ]
        rows = list(self.col.aggregate(pipeline))
        return [(r["_id"], float(r["revenue"])) for r in rows]

    def revenue_monthly(self) -> List[Tuple[str, float]]:
        pipeline = [
            {"$group": {"_id": {"$dateToString": {"format": "%Y-%m", "date": "$created_at"}}, "revenue": {"$sum": "$total"}}},
            {"$sort": {"_id": -1}},
        ]
        rows = list(self.col.aggregate(pipeline))
        return [(r["_id"], float(r["revenue"])) for r in rows]

    def get(self, id: int) -> Optional[Sale]:
        doc = self.col.find_one({"id": int(id)})
        return _to_model(doc) if doc else None
