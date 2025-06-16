from fastapi import Depends, HTTPException, status
from dependencies.auth_dependency import get_current_user
from models.user import User

def admin_required(current_user: User = Depends(get_current_user)) -> User:
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required."
        )
    return current_user
