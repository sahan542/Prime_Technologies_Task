from pydantic import BaseModel
from typing import Optional

class CartItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float  # price snapshot

class CartItemCreate(CartItemBase):
    user_id: int  # assuming frontend passes user_id for now

class CartItemUpdate(BaseModel):
    quantity: int

class CartItem(CartItemBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
