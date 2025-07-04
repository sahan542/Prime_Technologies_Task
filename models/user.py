from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session, relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    # Relationship to orders (One-to-Many)
    orders = relationship("Order", back_populates="user", cascade="all, delete")

# 🔍 Utility function to fetch a user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
