from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class LocalOrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderBase(BaseModel):
    # User details
    full_name: str
    full_address: str
    phone_no: str
    email: EmailStr
    country: str
    order_notes: Optional[str] = None
    inside_dhaka: bool

    # Shipping details
    shipping_method: str  # 'outside' or 'colombo'
    shipping_cost: float
    service_fee: float
    total_price: float  # Total price for the order

    # Payment details
    payment_method: str  # 'COD', 'card', etc.
    status: Optional[str] = "Pending"
    payment_status: Optional[str] = "Unpaid"

class OrderCreate(OrderBase):
    user_id: Optional[int] = None
    items: List[LocalOrderItemCreate]  # List of items in the order

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    payment_status: Optional[str] = None

class Order(OrderBase):
    id: Optional[int]  # Make id optional
    created_at: Optional[datetime]  # Make created_at optional
    updated_at: Optional[datetime]  # Make updated_at optional
    items: List[LocalOrderItemCreate] = []  # Each order will have a list of items

    class Config:
        orm_mode = True  # This allows Pydantic to work with SQLAlchemy models
