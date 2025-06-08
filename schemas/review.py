from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    user_name: str
    rating: int
    comment: Optional[str]

class ReviewCreate(ReviewBase):
    product_id: int

class Review(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
