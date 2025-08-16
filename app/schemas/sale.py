from datetime import datetime
from pydantic import BaseModel, Field

class SaleCreate(BaseModel):
    medicine_id: int
    quantity: int = Field(ge=1)
    unit_price: float = Field(ge=0)

class SaleOut(BaseModel):
    id: int
    medicine_id: int
    quantity: int
    unit_price: float
    total: float
    created_at: datetime
    class Config:
        from_attributes = True