from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.wishlist import WishlistItem
from schemas.wishlist import WishlistItemCreate, WishlistItem as WishlistItemSchema
from database import get_db

router = APIRouter()

@router.get("/wishlist/", response_model=list[WishlistItemSchema])
def get_wishlist(user_id: int, db: Session = Depends(get_db)):
    return db.query(WishlistItem).filter(WishlistItem.user_id == user_id).all()

@router.post("/wishlist/", response_model=WishlistItemSchema)
def add_to_wishlist(item: WishlistItemCreate, db: Session = Depends(get_db)):
    existing = db.query(WishlistItem).filter(
        WishlistItem.user_id == item.user_id,
        WishlistItem.product_id == item.product_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Item already in wishlist")

    db_item = WishlistItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/wishlist/{item_id}")
def remove_from_wishlist(item_id: int, db: Session = Depends(get_db)):
    item = db.query(WishlistItem).filter(WishlistItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"detail": "Item removed from wishlist"}
