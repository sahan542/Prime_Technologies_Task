from sqlalchemy import Column, Integer, UniqueConstraint
from database import Base

class WishlistItem(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="unique_user_product_wishlist"),
    )
