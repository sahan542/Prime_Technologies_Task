from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# -----------------------------
# Shared base schema
# -----------------------------
class ProductBase(BaseModel):
    slug: str
    title: str
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    img: Optional[str] = None
    sold_recently: Optional[int] = 0
    benefits: Optional[List[str]] = []

# -----------------------------
# Schema for product creation
# -----------------------------
class ProductCreate(ProductBase):
    pass

# -----------------------------
# Schema for product update (all optional)
# -----------------------------
class ProductUpdate(BaseModel):
    slug: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    img: Optional[str] = None
    sold_recently: Optional[int] = None
    benefits: Optional[List[str]] = None

# -----------------------------
# Response schema
# -----------------------------
class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
