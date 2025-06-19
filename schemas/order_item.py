from pydantic import BaseModel

# Base class used for shared fields
class OrderItemBase(BaseModel):
    product_id: str
    quantity: int

# ✅ Creation schema — includes all fields needed during POST
class OrderItemCreate(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int

# ✅ Response schema — used when returning from DB
class OrderItem(OrderItemBase):
    id: int
    order_id: int
    name: str
    price: float

    class Config:
        from_attributes = True  # 🔄 Use this for Pydantic v2 (replaces orm_mode)
