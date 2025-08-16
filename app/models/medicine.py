from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field

class Medicine(SQLModel, table=True):
    __tablename__ = "medicines"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    manufacturer: Optional[str] = Field(default=None, index=True)
    expiry_date: Optional[date] = None
    price: float = Field(default=0.0, ge=0)
    quantity: int = Field(default=0, ge=0)
