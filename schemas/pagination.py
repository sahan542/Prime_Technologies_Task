from pydantic import BaseModel
from typing import List
from schemas.user import UserOut  # Import UserOut schema

class PaginatedUsersResponse(BaseModel):
    users: List[UserOut]
    total_count: int
    total_pages: int
    current_page: int
