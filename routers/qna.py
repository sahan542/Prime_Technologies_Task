from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.qna import QnA
from models.user import User
from schemas.qna import QnACreate, QnAResponse
from dependencies.auth_dependency import get_current_user
from database import get_db

router = APIRouter()

@router.post("/qna/ask", response_model=QnAResponse)
def ask_question(
    qna: QnACreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_qna = QnA(
        product_id=qna.product_id,
        user_email=current_user.email,
        question=qna.question,
        answer="",
        is_public=False  # ✅ set here
    )
    db.add(new_qna)
    db.commit()
    db.refresh(new_qna)
    return new_qna



