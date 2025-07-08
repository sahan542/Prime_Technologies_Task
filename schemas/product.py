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

    totalReviews: Optional[int] = Field(0, alias="total_reviews")
    averageRatings: Optional[float] = Field(0.0, alias="average_ratings")
    salesCount: Optional[int] = Field(0, alias="sales_count")
    isDeleted: Optional[bool] = Field(False, alias="is_deleted")
    __v: Optional[int] = 0

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True 


class ProductMini(BaseModel):
    id: Union[int, str]
    title: str
    image: Optional[str] = Field(None, alias="img")
    price: float

    class Config:
        from_attributes = True
        populate_by_name = True