# schemas/cart.py

from pydantic import BaseModel
from typing import List, Optional
from models.cart import CartItem  # Ensure this import points to the CartItem model in the models folder


class CartItem(BaseModel):
    product_id: int  # The product's ID
    quantity: int  # The quantity of the product in the cart

    class Config:
        orm_mode = True


class CartInResponse(BaseModel):
    user_id: int  # The user ID for the cart
    items: List[CartItem]  # A list of cart items

    class Config:
        orm_mode = True


class CartCreate(BaseModel):
    user_id: int  # The user ID for cart creation
    items: List[CartItem]  # A list of cart items when creating a cart

    class Config:
        orm_mode = True


# New schema for updating quantity in cart item
class CartItemUpdate(BaseModel):
    quantity: int  

    class Config:
        orm_mode = True
