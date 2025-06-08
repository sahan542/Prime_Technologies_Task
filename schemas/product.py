from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    slug: str
    title: str
    description: Optional[str]
    price: float
    original_price: Optional[float]
    category: Optional[str]
    brand: Optional[str]
    img: Optional[str]
    sold_recently: Optional[int] = 0
    benefits: List[str]

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
