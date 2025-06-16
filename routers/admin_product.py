from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product as ProductModel
from models.user import User
from schemas.product import ProductCreate, ProductUpdate, Product as ProductSchema
from dependencies.admin_dependency import admin_required
from fastapi.responses import StreamingResponse
import csv
from io import StringIO
router = APIRouter(
    prefix="/api/admin/products",
    tags=["Admin Products"]
)

@router.post("/", response_model=ProductSchema)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    # Check for duplicate slug
    existing = db.query(ProductModel).filter(ProductModel.slug == product.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product with this slug already exists")

    # Ensure 'benefits' is a list (not a JSON string)
    product_data = product.dict()
    if isinstance(product_data.get("benefits"), str):
        import json
        try:
            product_data["benefits"] = json.loads(product_data["benefits"])
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON format for benefits")

    new_product = ProductModel(**product_data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.put("/{id}", response_model=ProductSchema)
def update_product(
    id: int,
    updated_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{id}")
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}

@router.put("/{id}/visibility", response_model=ProductSchema)
def toggle_visibility(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.visible = not product.visible
    db.commit()
    db.refresh(product)
    return product


@router.get("/export", response_class=StreamingResponse)
def export_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    products = db.query(ProductModel).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Title", "Slug", "Price", "Original Price",
        "Category", "Brand", "Visible", "Created At"
    ])

    for p in products:
        writer.writerow([
            p.id, p.title, p.slug, p.price, p.original_price,
            p.category, p.brand, p.visible, p.created_at
        ])

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=products.csv"}
    )