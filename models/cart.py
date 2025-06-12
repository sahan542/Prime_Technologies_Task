# models/cart.py

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List

# Base class for all SQLAlchemy models
Base = declarative_base()

# SQLAlchemy ORM Model for Cart
class Cart(Base):
    __tablename__ = 'cart'
    
    user_id = Column(Integer, primary_key=True)  # Cart is unique for each user
    items = relationship('CartItem', backref='cart', lazy=True)  # One-to-many relationship with CartItem

# SQLAlchemy ORM Model for CartItem
class CartItem(Base):
    __tablename__ = 'cart_item'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    cart_id = Column(Integer, ForeignKey('cart.user_id'), nullable=False)  # Foreign key referencing Cart
    
# Pydantic model for CartItem (for FastAPI validation)
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy models

# Pydantic model for Cart (for FastAPI validation)
class CartCreate(BaseModel):
    user_id: int
    items: List[CartItemCreate]

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy models

# Pydantic model for Cart response (for returning data to API users)
class CartInResponse(BaseModel):
    user_id: int
    items: List[CartItemCreate]

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy models
