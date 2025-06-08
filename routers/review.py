from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.review import Review
from schemas.review import ReviewCreate, Review as ReviewSchema

router = APIRouter()

@router.post("/reviews/", response_model=ReviewSchema)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/reviews/product/{product_id}", response_model=list[ReviewSchema])
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.product_id == product_id).all()
