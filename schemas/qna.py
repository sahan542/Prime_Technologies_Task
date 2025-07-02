from pydantic import BaseModel
from datetime import datetime

class QnACreate(BaseModel):
    product_id: int
    question: str

class QnAResponse(BaseModel):
    qna_id: int
    product_id: int
    user_email: str
    question: str
    answer: str
    is_public: bool
    created_at: datetime

    class Config:
        from_attributes = True

class QnAStatusUpdate(BaseModel):
    is_public: bool


class QnAAnswerUpdate(BaseModel):
    answer: str


