from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  # Import List from typing
from database import get_db
import models
from schemas.order import Order, OrderCreate, OrderUpdate
from models.order import Order as OrderModel
from models.order_item import OrderItem as OrderItemModel
from models.product import Product  # Import Product model
from auth.routes import get_current_user
from models.user import User
import traceback
from models.order_item import OrderItem

router = APIRouter(prefix="/api/admin", tags=["Admin"])

# 🚀 Create Order (Checkout)
# router = APIRouter(prefix="/api/admin", tags=["Admin"])
@router.post("/orders")
def create_order(data: dict, db: Session = Depends(get_db)):
    # Create the order first
    order = Order(
        full_name=data['full_name'],
        full_address=data['full_address'],
        phone_no=data['phone_no'],
        email=data['email'],
        country=data['country'],
        order_notes=data['order_notes'],
        inside_dhaka=data['inside_dhaka'],
        shipping_method=data['shipping_method'],
        shipping_cost=data['shipping_cost'],
        service_fee=data['service_fee'],
        total_price=data['total_price'],
        payment_method=data['payment_method'],
        user_id=data['user_id']
    )
    db.add(order)
    db.commit()  # Commit to get the order ID

    # Now, add items to the order_items table
    for item in data['items']:
        # Fetch product data to get product details like name and price
        product = db.query(Product).filter_by(id=item['product']).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        order_item = OrderItem(
            product_id=item['product'],  # Product ID
            order_id=order.id,  # Foreign key to the order
            quantity=item['quantity'],
            name=product.title,  # Use the product's title
            price=product.price  # Use the product's price
        )
        db.add(order_item)
    
    db.commit()  # Commit the transaction to save the order and order items

    return {"message": "Order created successfully!", "order_id": order.id}

# 👤 Get all orders for current user
@router.get("/me", response_model=List[Order])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(OrderModel).filter(OrderModel.user_id == current_user.id).all()


# 🛠 Update order status/payment
@router.patch("/{order_id}", response_model=Order)
def update_order_status(
    order_id: int,
    updates: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(OrderModel).filter(OrderModel.id == order_id, OrderModel.user_id == current_user.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if updates.status:
        order.status = updates.status
    if updates.payment_status:
        order.payment_status = updates.payment_status

    db.commit()
    db.refresh(order)
    return order
