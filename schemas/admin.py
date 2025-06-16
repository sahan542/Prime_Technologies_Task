# schemas/admin.py

from pydantic import BaseModel

class UpdateAdminStatus(BaseModel):
    is_admin: bool

    class Config:
        from_attributes = True 
