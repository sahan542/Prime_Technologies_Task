from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.review import Review
from schemas.review import ReviewCreate, Review as ReviewSchema
from dependencies.auth_dependency import get_current_user  
from models.user import User

router = APIRouter()

@router.post("/reviews/add-new", response_model=ReviewSchema)
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_review = Review(
        product_id=review.product_id,
        rating=review.rating,
        comment=review.comment,
        user_name=current_user.email,  # ✅ Use email as user_name
        is_public=False
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/reviews/product/{product_id}", response_model=list[ReviewSchema])
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    # Fetch only reviews where is_public is True
    reviews = db.query(Review).filter(Review.product_id == product_id, Review.is_public == True).all()
    return reviews
