from datetime import datetime, timedelta
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

# ✅ Load .env variables before accessing them
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # optional constant

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    # ✅ Ensure "sub" is explicitly set to email
    if "email" in data:
        to_encode["sub"] = data["email"]

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
