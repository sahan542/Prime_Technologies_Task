from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool  # 👈 Added this line

    class Config:
        from_attributes = True  # 👈 Replaces orm_mode in Pydantic v2
