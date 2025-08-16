from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Sale(SQLModel, table=True):
    __tablename__ = "sales"
    id: Optional[int] = Field(default=None, primary_key=True)
    medicine_id: int = Field(foreign_key="medicines.id")
    quantity: int = Field(ge=1)
    unit_price: float = Field(ge=0)
    total: float = Field(ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
