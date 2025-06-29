from pydantic import BaseModel
from typing import Optional

# Base class used for shared fields
class OrderItemBase(BaseModel):
    product_id: int  # Changed to int instead of str
    quantity: int

# ✅ Creation schema — includes all fields needed during POST
class OrderItemCreate(OrderItemBase):
    name: str
    price: float

# ✅ Response schema — used when returning from DB
class OrderItem(OrderItemBase):
    id: int
    order_id: int
    name: str
    price: float
    product_name: Optional[str]  # Add product_name field in the response schema
    product_price: Optional[float]  # Add product_price field in the response schema

    class Config:
        from_attributes = True  # Use this for Pydantic v2 (replaces orm_mode)
