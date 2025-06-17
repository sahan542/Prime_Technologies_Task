from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .order_item import OrderItemCreate, OrderItem  # Ensure these imports are correct

# 🛒 Each item in the order
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

# 🎯 Shared fields for creating/updating
class OrderBase(BaseModel):
    user_id: int
    total_amount: float
    status: Optional[str] = "Pending"
    payment_status: Optional[str] = "Unpaid"

# 🆕 For creating orders with items
class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

# ✏️ For partial updates
class OrderUpdate(BaseModel):
    status: Optional[str] = None
    payment_status: Optional[str] = None

# ✅ Full response model
class Order(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    items: Optional[List[OrderItem]] = []  # Correct use of `OrderItem` schema for items

    class Config:
        orm_mode = True  # This allows SQLAlchemy models to be used with Pydantic models
