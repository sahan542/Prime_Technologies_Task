from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    description: str

class Product(ProductCreate):
    id: int

    class Config:
        from_attributes = True

