from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.order import Order, OrderCreate, OrderUpdate


from models.order import Order as OrderModel
from models.order_item import OrderItem as OrderItemModel
from schemas.order import OrderCreate, Order, OrderUpdate
from database import get_db
from auth.routes import get_current_user
from models.user import User

router = APIRouter(prefix="/orders", tags=["Orders"])

# 🚀 Create Order (Checkout)
@router.post("/", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = OrderModel(**order.dict(exclude={"items"}))
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        db_item = OrderItemModel(
            order_id=db_order.id,
            product_id=item.product_id,
            name=item.name,
            price=item.price,
            quantity=item.quantity
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_order)
    return db_order


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
