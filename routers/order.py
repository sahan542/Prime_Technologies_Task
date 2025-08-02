from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  # Import List from typing
from database import get_db
import models
from schemas.order import Order, OrderCreate, OrderUpdate
from models.order import Order as OrderModel
from models.order_item import OrderItem as OrderItemModel
from models.product import Product  # Import Product model
from auth.routes import get_current_user
from models.user import User
import traceback
from models.order_item import OrderItem
from datetime import datetime, timedelta
from sqlalchemy import func


router = APIRouter(prefix="/api/admin", tags=["Admin"])

# 🚀 Create Order (Checkout)
# router = APIRouter(prefix="/api/admin", tags=["Admin"])
@router.post("/orders")
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    try:
        # Step 1: Create Order
        order = OrderModel(
            full_name=data.full_name,
            full_address=data.full_address,
            phone_no=data.phone_no,
            email=data.email,
            country=data.country,
            order_notes=data.order_notes,
            inside_dhaka=data.inside_dhaka,
            shipping_method=data.shipping_method,
            shipping_cost=data.shipping_cost,
            service_fee=data.service_fee,
            total_price=data.total_price,
            payment_method=data.payment_method,
            payment_status=data.payment_status,
            status=data.status,
            user_id=data.user_id  # ✅ Assign it here
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        # Step 2: Add Order Items
        for item in data.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found")

            order_item = OrderItemModel(
                product_id=item.product_id,
                order_id=order.id,
                quantity=item.quantity,
                name=product.title,
                price=product.price
            )
            db.add(order_item)

        db.commit()

        return {"message": "Order created successfully!", "order_id": order.id}

    except Exception as e:
        db.rollback()
        print("❌ Order creation error:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Order creation failed.")

# 👤 Get all orders for current user
@router.get("/me", response_model=List[Order])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(OrderModel).filter(OrderModel.user_id == current_user.id).all()


# 🛠 Update order status/payment
@router.patch("/{order_id}", response_model=Order)
def update_order_status(
    order_id: int,
    updates: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(OrderModel).filter(OrderModel.id == order_id, OrderModel.user_id == current_user.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if updates.status:
        order.status = updates.status
    if updates.payment_status:
        order.payment_status = updates.payment_status

    db.commit()
    db.refresh(order)
    return order


# 🧾 Get order by order ID
@router.get("/orders/{order_id}", response_model=Order)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(OrderModel).filter(OrderModel.id == order_id, OrderModel.user_id == current_user.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


# 🚀 Get total sales for each day in the last 7 days
@router.get("/sales/last-seven-days", response_model=List[float])
def get_sales_last_seven_days(db: Session = Depends(get_db)):
    try:
        # Calculate the start and end of the last 7 days
        today = datetime.now()
        last_seven_days = [today - timedelta(days=i) for i in range(7)]

        # Query the database to get the total sales for each of the last 7 days
        sales_data = []
        for day in last_seven_days:
            start_of_day = day.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = day.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            # Query to get total sales for each day
            total_sales = db.query(func.sum(OrderModel.total_price)) \
                .filter(OrderModel.created_at >= start_of_day, OrderModel.created_at <= end_of_day) \
                .scalar()  # scalar() returns the first column of the first row

            sales_data.append(total_sales if total_sales else 0)

        return sales_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sales data: {str(e)}")
    


# 🚀 Get count and percentage of each order status (Pending, Dispatched, Returned)
@router.get("/order-dispatch-status", response_model=List[dict])
def get_order_dispatch_status(db: Session = Depends(get_db)):
    try:
        # Get total count of orders (total number of orders in the table)
        total_orders = db.query(func.count(OrderModel.id)).scalar()

        if total_orders == 0:
            raise HTTPException(status_code=400, detail="No orders found.")

        # Count orders with "Pending" status
        pending_count = db.query(func.count(OrderModel.id)).filter(OrderModel.status.ilike("Pending")).scalar()

        # Count orders with "Dispatched" status
        dispatched_count = db.query(func.count(OrderModel.id)).filter(OrderModel.status.ilike("Dispatched")).scalar()

        # Count orders with "Returned" status
        returned_count = db.query(func.count(OrderModel.id)).filter(OrderModel.status.ilike("Returned")).scalar()

        # Calculate percentages for each status
        pending_percentage = (pending_count / total_orders) * 100 if total_orders > 0 else 0
        dispatched_percentage = (dispatched_count / total_orders) * 100 if total_orders > 0 else 0
        returned_percentage = (returned_count / total_orders) * 100 if total_orders > 0 else 0

        # Ensure all statuses are returned even if the count is 0
        status_data = [
            {
                "status": "Pending",
                "count": pending_count,
                "percentage": pending_percentage
            },
            {
                "status": "Dispatched",
                "count": dispatched_count,
                "percentage": dispatched_percentage
            },
            {
                "status": "Returned",
                "count": returned_count,
                "percentage": returned_percentage
            }
        ]

        # Return the percentages with count for all three statuses
        return status_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating dispatch status: {str(e)}")