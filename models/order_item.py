from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)  # Correct foreign key
    name = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")  # Add reverse relationship
    product = relationship("Product", back_populates="order_items")  # Add relationship to Product model

