from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.order import Order as OrderModel
from models.order_item import OrderItem as OrderItemModel
from schemas.order import OrderCreate, OrderUpdate, Order as OrderSchema
from schemas.order_item import OrderItemCreate
from dependencies.admin_dependency import admin_required
from models.user import User
from sqlalchemy.orm import joinedload


router = APIRouter(
    prefix="/api/admin/orders",
    tags=["Admin Orders"]
)

@router.post("/", response_model=OrderSchema)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    # Create order
    new_order = OrderModel(
        user_id=order_data.user_id,
        total_amount=order_data.total_amount,
        status=order_data.status,
        payment_status=order_data.payment_status
    )
    db.add(new_order)
    db.flush()  # Get new_order.id before commit

    # Add each order item
    for item in order_data.items:
        db.add(OrderItemModel(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        ))

    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/", response_model=list[OrderSchema])
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    return db.query(OrderModel).all()


@router.put("/{order_id}", response_model=OrderSchema)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    for field, value in order.dict(exclude_unset=True).items():
        setattr(db_order, field, value)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted successfully"}


@router.get("/{order_id}", response_model=OrderSchema)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Load items manually
    order.items = db.query(OrderItemModel).filter(OrderItemModel.order_id == order.id).all()
    return order

@router.put("/{order_id}/status", response_model=OrderSchema)
def update_order_status(
    order_id: int,
    status_update: dict,  # expects { "status": "shipped" }
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    status = status_update.get("status")
    if status:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
        return db_order
    else:
        raise HTTPException(status_code=400, detail="Status is required")



@router.get("/user/{user_id}", response_model=list[OrderSchema])
def get_orders_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    orders = db.query(OrderModel).filter(OrderModel.user_id == user_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")

    return orders


# Endpoint to update the payment_status (Unpaid -> Paid)
@router.put("/{order_id}/payment_status", response_model=OrderSchema)
def update_payment_status(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if db_order.payment_status != "Unpaid":
        raise HTTPException(status_code=400, detail="Order is not in 'Unpaid' status")

    db_order.payment_status = "Paid"
    db.commit()
    db.refresh(db_order)
    return db_order

