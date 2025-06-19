from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .order_item import OrderItem  # ✅ Only import the response schema


# 🛒 Each item in the order (already exists)
class LocalOrderItemCreate(BaseModel):
    product_id: str  # updated to match your frontend: string id
    name: str
    price: float
    quantity: int


# 🎯 Shared base model for orders
class OrderBase(BaseModel):
    # user_id: int

    # Billing fields
    first_name: str
    last_name: str
    street_address: str
    apartment: Optional[str] = None
    city: str
    phone: str
    email: EmailStr

    create_account: Optional[bool] = False
    ship_different: Optional[bool] = False
    order_notes: Optional[str] = None

    # Summary
    shipping_method: str  # 'outside' or 'colombo'
    shipping_cost: float
    service_fee: float
    total_amount: float

    # Payment
    payment_method: str  # 'cod', 'card', etc.
    status: Optional[str] = "Pending"
    payment_status: Optional[str] = "Unpaid"


# 🆕 For creating orders (includes cart items)
class OrderCreate(OrderBase):
    items: List[LocalOrderItemCreate]


# ✏️ For updating order status or payment
class OrderUpdate(BaseModel):
    status: Optional[str] = None
    payment_status: Optional[str] = None


# ✅ Full response schema
class Order(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    items: List[OrderItem] = []

class Config:
    from_attributes = True

