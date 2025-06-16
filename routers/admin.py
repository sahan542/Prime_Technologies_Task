# routers/admin.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.admin import UpdateAdminStatus  # import this


from dependencies.admin_dependency import admin_required
from dependencies.auth_dependency import get_current_user
from database import get_db
from models.user import User
from schemas.user import UserOut

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