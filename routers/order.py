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
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    try:
        # Step 1: Create Order
        order = OrderModel(
            full_name=data.full_name,
            full_address=data.full_address,
            phone_no=data.phone_no,
            email=data.email,
            country=data.country,
            order_notes=data.order_notes,
            inside_dhaka=data.inside_dhaka,
            shipping_method=data.shipping_method,
            shipping_cost=data.shipping_cost,
            service_fee=data.service_fee,
            total_price=data.total_price,
            payment_method=data.payment_method,
            payment_status=data.payment_status,
            status=data.status,
            user_id=data.user_id  # ✅ Assign it here
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        # Step 2: Add Order Items
        for item in data.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found")

            order_item = OrderItemModel(
                product_id=item.product_id,
                order_id=order.id,
                quantity=item.quantity,
                name=product.title,
                price=product.price
            )
            db.add(order_item)

        db.commit()

        return {"message": "Order created successfully!", "order_id": order.id}

    except Exception as e:
        db.rollback()
        print("❌ Order creation error:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Order creation failed.")

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


# 🧾 Get order by order ID
@router.get("/orders/{order_id}", response_model=Order)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(OrderModel).filter(OrderModel.id == order_id, OrderModel.user_id == current_user.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order
