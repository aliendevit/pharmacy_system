from typing import Optional
from datetime import date
from pydantic import BaseModel, Field

class MedicineBase(BaseModel):
    name: str = Field(min_length=1)
    manufacturer: Optional[str] = None
    expiry_date: Optional[date] = None
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)

class MedicineCreate(MedicineBase):
    pass

class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    manufacturer: Optional[str] = None
    expiry_date: Optional[date] = None
    price: Optional[float] = Field(default=None, ge=0)
    quantity: Optional[int] = Field(default=None, ge=0)

class MedicineOut(MedicineBase):
    id: int
    class Config:
        from_attributes = True