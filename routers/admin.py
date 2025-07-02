# routers/admin.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.admin import UpdateAdminStatus  # import this
from models.user import User as UserModel



from dependencies.admin_dependency import admin_required
from dependencies.auth_dependency import get_current_user
from database import get_db
from models.user import User
from schemas.user import UserOut
from fastapi.responses import StreamingResponse
import csv
from io import StringIO
from models.order import Order as OrderModel
from models.order_item import OrderItem as OrderItemModel
from schemas.order import OrderCreate, OrderUpdate, Order as OrderSchema
from sqlalchemy.orm import joinedload


router = APIRouter(prefix="/admin", tags=["Admin"])

# Dashboard Overview
@router.get("/dashboard", summary="Admin dashboard overview")
def get_admin_dashboard(current_user=Depends(admin_required)):
    return {"msg": "Welcome Admin", "user": current_user.email}

# Get All Users
@router.get("/users", response_model=list[UserOut], summary="List all users (admin only)")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    users = db.query(User).all()
    return users



@router.delete("/users/{user_id}", summary="Delete a user by ID", status_code=204)
def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return None  # 204 No Content


@router.put("/users/{user_id}/admin-status", summary="Update user's is_admin status", response_model=UserOut)
def update_admin_status(
    user_id: int,
    data: UpdateAdminStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_admin = data.is_admin
    db.commit()
    db.refresh(user)
    return user


@router.get("/users/export", response_class=StreamingResponse)
def export_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    users = db.query(User).all()

    output = StringIO()
    writer = csv.writer(output)

    # Corrected header (no "Username")
    writer.writerow(["ID", "Email", "Is Admin", "Created At", "Updated At"])

    for user in users:
        writer.writerow([
            user.id,
            user.email,
            user.is_admin,
            user.created_at.isoformat() if hasattr(user, 'created_at') and user.created_at else '',
            user.updated_at.isoformat() if hasattr(user, 'updated_at') and user.updated_at else ''
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=users.csv"}
    )


@router.get("/orders", response_model=list[OrderSchema], summary="Get all orders")
def get_all_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    """
    This endpoint retrieves all orders from the database.
    It handles the `/api/admin/orders` route.
    """
    # Query all orders in the database
    orders = db.query(OrderModel).all()

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    return orders




# Corrected endpoint for getting all orders
@router.get("/", response_model=list[OrderSchema], summary="Get all orders")
def get_all_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    """
    This endpoint retrieves all orders from the database.
    It handles the `/api/admin/orders` route.
    """
    # Query all orders in the database
    orders = db.query(OrderModel).all()

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    return orders
