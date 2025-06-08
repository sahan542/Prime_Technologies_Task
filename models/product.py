from sqlalchemy import Column, Integer, String, Numeric, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import ARRAY
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    img = Column(String)
    category = Column(String)
    price = Column(Numeric(10, 2), nullable=False)
    original_price = Column(Numeric(10, 2))
    description = Column(Text)
    sold_recently = Column(Integer, default=0)
    brand = Column(String)
    benefits = Column(ARRAY(Text))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
