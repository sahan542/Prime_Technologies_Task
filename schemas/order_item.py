from pydantic import BaseModel

# Base model for order items with common fields
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

# Model used for creating order items (inherits from OrderItemBase)
class OrderItemCreate(OrderItemBase):
    pass  # No additional fields for creation; just inherits OrderItemBase

# Full model for order items, including ID and associated order ID
class OrderItem(OrderItemBase):
    id: int
    order_id: int  # Reference to the order that the item belongs to

    class Config:
        orm_mode = True  # This allows SQLAlchemy models to be used with Pydantic models
