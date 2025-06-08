from pydantic import BaseModel
from typing import List

class BulkCartProductEntry(BaseModel):
    product_id: int
    quantity: int

class UnifiedCartRequest(BaseModel):
    user_id: int
    products: List[BulkCartProductEntry]

class CartItemUpdate(BaseModel):
    quantity: int

class CartItem(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        orm_mode = True
