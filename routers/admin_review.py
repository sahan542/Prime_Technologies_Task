from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.review import Review
from models.user import User
from schemas.review import Review as ReviewSchema
from dependencies.auth_dependency import get_current_user
from database import get_db

router = APIRouter()


def require_admin(user: User):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    return user


# ✅ Get all reviews
@router.get("/admin/reviews", response_model=list[ReviewSchema])
def get_all_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    return db.query(Review).order_by(Review.created_at.desc()).all()


# ✅ Update is_public status (approve/unapprove)
@router.patch("/admin/reviews/{review_id}", response_model=ReviewSchema)
def update_review_visibility(
    review_id: int,
    is_public: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review.is_public = is_public
    db.commit()
    db.refresh(review)
    return review


# ✅ Delete a review
@router.delete("/admin/reviews/{review_id}", status_code=204)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()
    return
