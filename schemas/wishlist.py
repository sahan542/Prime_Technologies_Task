from pydantic import BaseModel

class WishlistItemBase(BaseModel):
    user_id: int
    product_id: int

class WishlistItemCreate(WishlistItemBase):
    pass

class WishlistItem(WishlistItemBase):
    id: int

    class Config:
        orm_mode = True
