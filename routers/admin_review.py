from fastapi import APIRouter, Depends, HTTPException, status, Query
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


@router.get("/admin/reviews", response_model=dict, summary="Get all reviews with pagination")
def get_all_reviews(
    page: int = Query(1, ge=1),  # Page number (default 1, minimum 1)
    limit: int = Query(8, gt=0),  # Limit on the number of items per page (default to 8)
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    try:
        # Calculate the offset based on the page and limit
        offset = (page - 1) * limit

        # Query all reviews, ordered by creation date (descending)
        query = db.query(Review).order_by(Review.created_at.desc())

        # Get the total number of reviews
        total_reviews = query.count()

        # Fetch reviews for the current page
        reviews = query.offset(offset).limit(limit).all()

        if not reviews:
            raise HTTPException(status_code=404, detail="No reviews found")

        # Calculate total pages
        total_pages = (total_reviews // limit) + (1 if total_reviews % limit > 0 else 0)

        # Return the reviews along with pagination metadata
        return {
            "reviews": [ReviewSchema.from_orm(review) for review in reviews],  # Convert SQLAlchemy models to Pydantic models
            "currentPage": page,
            "totalPages": total_pages,
            "totalReviews": total_reviews,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


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
