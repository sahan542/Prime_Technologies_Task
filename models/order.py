from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP, func, Boolean, Text
from sqlalchemy.orm import relationship
from database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Billing info
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    street_address = Column(String, nullable=False)
    apartment = Column(String, nullable=True)
    city = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)

    create_account = Column(Boolean, default=False)
    ship_different = Column(Boolean, default=False)
    order_notes = Column(Text, nullable=True)

    # Pricing summary
    shipping_method = Column(String, nullable=False)  # 'outside' or 'colombo'
    shipping_cost = Column(Numeric(10, 2), nullable=False)
    service_fee = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)

    # Payment
    payment_method = Column(String, nullable=False)  # 'cod', 'card', 'installment', etc.
    payment_status = Column(String, default="Unpaid")  # Unpaid, Paid
    status = Column(String, default="Pending")  # Pending, Processing, etc.

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
