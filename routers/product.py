from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate, Product as ProductSchema, ProductMini

router = APIRouter()

# -----------------------------
# Create Product
# -----------------------------
@router.post("/products/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# -----------------------------
# List Products (with filters)
# -----------------------------
@router.get("/products/", response_model=List[ProductSchema])
def list_products(
    db: Session = Depends(get_db),
    category: Optional[List[str]] = Query(None),
    brand: Optional[List[str]] = Query(None),
    min_price: Optional[float] = 0,
    max_price: Optional[float] = 1_000_000,
    search: Optional[str] = None,
    limit: int = Query(50, gt=0),
    offset: int = Query(0, ge=0),
):
    try:
        query = db.query(Product).filter(Product.visible == True, Product.is_deleted == False)

        if category:
            query = query.filter(Product.category.in_(category))
        if brand:
            query = query.filter(Product.brand.in_(brand))
        if min_price is not None and max_price is not None:
            query = query.filter(Product.price.between(min_price, max_price))
        if search:
            pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Product.title.ilike(pattern),
                    Product.description.ilike(pattern),
                    Product.brand.ilike(pattern),
                    Product.category.ilike(pattern),
                )
            )

        return query.offset(offset).limit(limit).all()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# -----------------------------
# Get Product by Slug
# -----------------------------
@router.get("/products/{slug}", response_model=ProductSchema)
def get_product_by_slug(slug: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.slug == slug, Product.is_deleted == False).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# -----------------------------
# Update Product
# -----------------------------
@router.put("/products/{id}", response_model=ProductSchema)
def update_product(id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

# -----------------------------
# Delete Product (Soft delete)
# -----------------------------
@router.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.is_deleted = True
    db.commit()
    return {"detail": "Product deleted successfully"}

# -----------------------------
# Get Products by Category
# -----------------------------
@router.get("/products/category/{category}", response_model=List[ProductMini])
def get_products_by_category(category: str, db: Session = Depends(get_db)):
    products = db.query(Product).filter(
        Product.category == category,
        Product.visible == True,
        Product.is_deleted == False
    ).all()

    if not products:
        raise HTTPException(status_code=404, detail="No products found in this category")
    
    return products
