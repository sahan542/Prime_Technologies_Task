# routers/cart.py

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas.cart import CartCreate, CartInResponse, CartItem, CartItemUpdate  # <-- Import CartItemUpdate here
from database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# In-memory storage for simplicity, replace with real DB logic
fake_db = {}

# Create a new cart or update an existing one
@router.post("/cart", response_model=CartInResponse)
def create_or_update_cart(cart: CartCreate, db: Session = Depends(get_db)):
    if cart.user_id in fake_db:
        fake_db[cart.user_id].items.extend(cart.items)
    else:
        fake_db[cart.user_id] = cart
    return fake_db[cart.user_id]

# Get the cart for a user
@router.get("/cart/{user_id}", response_model=CartInResponse)
def get_cart(user_id: int, db: Session = Depends(get_db)):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="Cart not found")
    return fake_db[user_id]

# Delete a cart for a user
@router.delete("/cart/{user_id}")
def delete_cart(user_id: int, db: Session = Depends(get_db)):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="Cart not found")
    del fake_db[user_id]
    return {"message": "Cart deleted successfully"}

# Add an item to the cart
@router.post("/cart/{user_id}/add", response_model=CartInResponse)
def add_item_to_cart(user_id: int, item: CartItem, db: Session = Depends(get_db)):
    if user_id not in fake_db:
        fake_db[user_id] = {"user_id": user_id, "items": []}
    fake_db[user_id]["items"].append(item)
    return fake_db[user_id]

# Remove an item from the cart
@router.delete("/cart/{user_id}/remove/{product_id}", response_model=CartInResponse)
def remove_item_from_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart = fake_db[user_id]
    cart["items"] = [item for item in cart["items"] if item.product_id != product_id]
    return cart

# Update an item's quantity in the cart
@router.patch("/cart/{user_id}/update/{product_id}", response_model=CartInResponse)
def update_item_quantity(user_id: int, product_id: int, item: CartItemUpdate, db: Session = Depends(get_db)):
    # Check if user has a cart
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Access the user's cart
    cart = fake_db[user_id]

    # Try to find the product in the cart
    item_found = False
    for cart_item in cart["items"]:
        if cart_item.product_id == product_id:
            cart_item.quantity = item.quantity  # Update the quantity
            item_found = True
            break

    if not item_found:
        raise HTTPException(status_code=404, detail="Product not found in cart")

    # Return the updated cart
    return cart
