from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.password_handler import hash_password, verify_password
from auth.jwt_handler import create_access_token
from models.user import User
from schemas.user import UserCreate, UserLogin, UserOut
from database import get_db

router = APIRouter()

# ---------------------------------------
# Signup Route
# ---------------------------------------
@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ---------------------------------------
# Login (JSON body)
# ---------------------------------------
@router.post("/login", tags=["Auth"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # ✅ Store email in token payload
    token = create_access_token({"sub": db_user.email})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "id": db_user.id,
        "email": db_user.email
    }

# ---------------------------------------
# Login (OAuth2 Form)
# ---------------------------------------
@router.post("/login-form", tags=["Auth"])
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ Store email in token
    token = create_access_token({"sub": db_user.email})
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }
