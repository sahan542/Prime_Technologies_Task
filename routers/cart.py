from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.cart import CartItem
from models.product import Product
from schemas.cart import (
    CartItemUpdate,
    CartItem as CartItemSchema,
    BulkCartProductEntry,
    UnifiedCartRequest,
)

router = APIRouter()


@router.get("/cart/", response_model=list[CartItemSchema])
def get_cart(user_id: int, db: Session = Depends(get_db)):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()


@router.post("/cart/")
def add_to_cart(request: UnifiedCartRequest, db: Session = Depends(get_db)):
    # Step 1: Merge repeated product_id entries
    merged_products = defaultdict(int)
    for entry in request.products:
        merged_products[entry.product_id] += entry.quantity

    created_items = []

    for product_id, total_quantity in merged_products.items():
        # Step 2: Validate product
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            continue  # skip invalid product

        # Step 3: Check for existing cart item
        existing_item = db.query(CartItem).filter(
            CartItem.user_id == request.user_id,
            CartItem.product_id == product_id
        ).first()

        if existing_item:
            existing_item.quantity += total_quantity
            db.add(existing_item)
            created_items.append(existing_item)
        else:
            new_item = CartItem(
                user_id=request.user_id,
                product_id=product_id,
                quantity=total_quantity,
                price=float(product.price),
            )
            db.add(new_item)
            created_items.append(new_item)

    db.commit()
    return {"detail": f"{len(created_items)} cart item(s) processed successfully."}
