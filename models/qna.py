from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from database import Base

class QnA(Base):
    __tablename__ = "qna"

    qna_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    user_email = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, default="", nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)  # ✅ NEW
    created_at = Column(String, default=func.now())
