from typing import Iterable, Optional, List, Tuple
from datetime import datetime
from sqlmodel import select, text
from app.models.sale import Sale

class SalesRepoSQL:
    def __init__(self, session):
        self.session = session

    def create(self, s: Sale) -> Sale:
        self.session.add(s)
        self.session.commit()
        self.session.refresh(s)
        return s

    def list(self, *, since: Optional[datetime] = None, until: Optional[datetime] = None) -> Iterable[Sale]:
        stmt = select(Sale)
        if since:
            stmt = stmt.where(Sale.created_at >= since)
        if until:
            stmt = stmt.where(Sale.created_at < until)
        stmt = stmt.order_by(Sale.created_at.desc())
        return list(self.session.exec(stmt))

    def revenue_daily(self) -> List[Tuple[str, float]]:
        q = text("""
            SELECT date(created_at) as day, SUM(total) as revenue
            FROM sales
            GROUP BY day
            ORDER BY day DESC
        """)
        rows = self.session.exec(q).all()
        return [(r[0], float(r[1] or 0)) for r in rows]

    def revenue_monthly(self) -> List[Tuple[str, float]]:
        q = text("""
            SELECT strftime('%Y-%m', created_at) as month, SUM(total) as revenue
            FROM sales
            GROUP BY month
            ORDER BY month DESC
        """)
        rows = self.session.exec(q).all()
        return [(r[0], float(r[1] or 0)) for r in rows]
