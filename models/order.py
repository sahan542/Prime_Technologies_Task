from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, default="Pending")  # Pending, Processing, Shipped, Delivered, Cancelled
    payment_status = Column(String, default="Unpaid")  # Unpaid, Paid
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="orders")
