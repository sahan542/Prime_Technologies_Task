from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    ForeignKey,
    TIMESTAMP,
    func,
    Boolean,
    Text
)
from sqlalchemy.orm import relationship
from database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Make nullable if guest checkout is supported

    # Billing Info
    full_name = Column(String, nullable=False)
    full_address = Column(String, nullable=False)
    phone_no = Column(String, nullable=False)
    email = Column(String, nullable=False)
    country = Column(String, nullable=False)
    order_notes = Column(Text, nullable=True)
    inside_dhaka = Column(Boolean, default=False)

    # Pricing Summary
    shipping_method = Column(String, nullable=False)
    shipping_cost = Column(Numeric(10, 2), nullable=False)
    service_fee = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)

    # Payment Info
    payment_method = Column(String, nullable=False)
    payment_status = Column(String, default="Unpaid")  # Can be: Unpaid, Paid, Refunded
    status = Column(String, default="Pending")         # Can be: Pending, Processing, Completed, Cancelled

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="orders")  # From User model: orders = relationship(...)
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
