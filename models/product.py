# from sqlalchemy import Column, Integer, String, Numeric, Text, TIMESTAMP, func, JSON, Boolean
# from sqlalchemy.dialects.postgresql import ARRAY
# from database import Base

# class Product(Base):
#     __tablename__ = "products"

#     id = Column(Integer, primary_key=True, index=True)
#     slug = Column(String, unique=True, nullable=False)
#     title = Column(String, nullable=False)
#     img = Column(String)
#     category = Column(String)
#     price = Column(Numeric(10, 2), nullable=False)
#     original_price = Column(Numeric(10, 2))
#     description = Column(Text)
#     sold_recently = Column(Integer, default=0)
#     brand = Column(String)
#     visible = Column(Boolean, default=True)
#     benefits = Column(JSON, default=[])
#     created_at = Column(TIMESTAMP, server_default=func.now())
#     updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Text,
    TIMESTAMP,
    func,
    JSON,
    Boolean,
    Float
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship  # ✅ required for back_populates
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)  # maps to `name`
    img = Column(String)  # maps to `image`
    category = Column(String)
    price = Column(Numeric(10, 2), nullable=False)
    original_price = Column(Numeric(10, 2))  # optional
    description = Column(Text)
    sold_recently = Column(Integer, default=0)
    brand = Column(String)
    visible = Column(Boolean, default=True)
    benefits = Column(JSON, default=[])

    # Newly added fields from the payload
    images = Column(ARRAY(String))                
    stock = Column(Integer, default=0)            
    discount = Column(Integer, nullable=True)      
    tags = Column(ARRAY(String), default=[])     
    total_reviews = Column(Integer, default=0)     
    average_ratings = Column(Float, default=0.0) 
    sales_count = Column(Integer, default=0)       
    is_deleted = Column(Boolean, default=False)   

    created_at = Column(TIMESTAMP, server_default=func.now())  
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now()) 

    # ✅ Relationship to OrderItem (required if back_populates is used in OrderItem)
    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete")
