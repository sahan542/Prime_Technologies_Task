from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session, relationship  # ✅ Added relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    orders = relationship("Order", back_populates="user", cascade="all, delete")

# 🔑 Utility function to fetch user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
