from fastapi import APIRouter, Depends, HTTPException, Query
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


@router.get("/products", response_model=dict, summary="Get all products with pagination")
def get_all_products(
    page: int = Query(1, ge=1),  # Page number (default to 1, minimum 1)
    limit: int = Query(8, gt=0),  # Limit on the number of items per page (default to 8)
    db: Session = Depends(get_db),  # Dependency to get the DB session
    current_user: User = Depends(admin_required)  # Ensure the user is an admin
):
    try:
        # Calculate the offset based on the page and limit
        offset = (page - 1) * limit

        # Start the query with the basic filter (fetch all products)
        query = db.query(ProductModel)

        # Get the total number of products
        total_products = query.count()

        # Fetch the products for the current page
        products = query.offset(offset).limit(limit).all()

        if not products:
            # Optional: Provide a friendly message if no products are found.
            raise HTTPException(status_code=404, detail="No products found for this page.")

        # Calculate total pages
        total_pages = (total_products // limit) + (1 if total_products % limit > 0 else 0)

        # Return the products along with pagination metadata
        return {
            "products": [ProductSchema.from_orm(product) for product in products],  # Convert SQLAlchemy models to Pydantic models
            "currentPage": page,
            "totalPages": total_pages,
            "totalProducts": total_products,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")




@router.put("/{id}/edit", response_model=ProductSchema)
def edit_product(
    id: int,
    updated_data: ProductCreate,  # Using ProductCreate for editing as it includes all necessary fields
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check for duplicate slug if the slug is being updated
    if updated_data.slug != product.slug:
        existing = db.query(ProductModel).filter(ProductModel.slug == updated_data.slug).first()
        if existing:
            raise HTTPException(status_code=400, detail="Product with this slug already exists")

    # Ensure 'benefits' is a list (not a JSON string)
    product_data = updated_data.dict()
    if isinstance(product_data.get("benefits"), str):
        import json
        try:
            product_data["benefits"] = json.loads(product_data["benefits"])
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON format for benefits")

    # Update the product with new data
    for key, value in product_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.get("/{id}", response_model=ProductSchema)
def get_product_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    # Fetch the product by its ID from the database
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    
    # If no product is found, raise a 404 HTTP exception
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Return the found product
    return product
