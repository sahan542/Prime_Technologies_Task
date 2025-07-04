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


@router.get("/qna/product/{product_id}", response_model=list[QnAResponse])
def get_qna_for_product(product_id: int, db: Session = Depends(get_db)):
    # Fetch all Q&A data for the specified product where is_public is True
    qna_data = db.query(QnA).filter(QnA.product_id == product_id, QnA.is_public == True).all()
    return qna_data



