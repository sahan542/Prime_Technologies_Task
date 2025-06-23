# from pydantic import BaseModel
# from typing import List, Optional
# from datetime import datetime

# # -----------------------------
# # Shared base schema
# # -----------------------------
# class ProductBase(BaseModel):
#     slug: str
#     title: str
#     description: Optional[str] = None
#     price: float
#     original_price: Optional[float] = None
#     category: Optional[str] = None
#     brand: Optional[str] = None
#     img: Optional[str] = None
#     sold_recently: Optional[int] = 0
#     benefits: Optional[List[str]] = []

# # -----------------------------
# # Schema for product creation
# # -----------------------------
# class ProductCreate(ProductBase):
#     pass

# # -----------------------------
# # Schema for product update (all optional)
# # -----------------------------
# class ProductUpdate(BaseModel):
#     slug: Optional[str] = None
#     title: Optional[str] = None
#     description: Optional[str] = None
#     price: Optional[float] = None
#     original_price: Optional[float] = None
#     category: Optional[str] = None
#     brand: Optional[str] = None
#     img: Optional[str] = None
#     sold_recently: Optional[int] = None
#     benefits: Optional[List[str]] = None

# # -----------------------------
# # Response schema
# # -----------------------------
# class Product(ProductBase):
#     id: int
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         from_attributes = True

from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

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

class ProductCreate(ProductBase):
    pass

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

# ✅ Updated response schema to match frontend shape
class Product(ProductBase):
    id: Union[int, str]  

    images: Optional[List[str]] = []
    stock: Optional[int] = 0
    discount: Optional[float] = 0
    tags: Optional[List[str]] = []
    totalReviews: Optional[int] = 0
    averageRatings: Optional[float] = 0.0
    salesCount: Optional[int] = 0
    isDeleted: Optional[bool] = False
    __v: Optional[int] = 0

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
