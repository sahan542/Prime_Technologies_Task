from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func, Boolean
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    user_name = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    is_public = Column(Boolean, default=False)  # 👈 Add this line
    created_at = Column(TIMESTAMP, server_default=func.now())
