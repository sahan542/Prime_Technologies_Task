from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TopProduct(BaseModel):
    id: int
    title: str
    sold_recently: int

    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    total_sales: float
    monthly_revenue: float
    top_products: List[TopProduct]
    active_users: int
