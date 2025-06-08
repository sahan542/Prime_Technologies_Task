from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product
from schemas.product import ProductCreate, Product as ProductSchema

router = APIRouter()

@router.post("/products/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/products/", response_model=list[ProductSchema])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/products/{slug}", response_model=ProductSchema)
def get_product_by_slug(slug: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.slug == slug).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{id}", response_model=ProductSchema)
def update_product(id: int, product_data: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product_data.dict().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}
