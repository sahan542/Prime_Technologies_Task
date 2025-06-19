from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.qna import QnA
from models.user import User
from schemas.qna import QnAResponse, QnAStatusUpdate, QnAAnswerUpdate
from dependencies.admin_dependency import admin_required

router = APIRouter(prefix="/api/admin/qna", tags=["Admin QnA"])

# 1. Get all QnAs
@router.get("/", response_model=list[QnAResponse])
def get_all_qnas(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    return db.query(QnA).all()

# 2. Update QnA status (is_public)
@router.patch("/{qna_id}/status", response_model=QnAResponse)
def update_qna_status(
    qna_id: int,
    data: QnAStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    qna = db.query(QnA).filter(QnA.qna_id == qna_id).first()
    if not qna:
        raise HTTPException(status_code=404, detail="QnA not found")
    qna.is_public = data.is_public
    db.commit()
    db.refresh(qna)
    return qna

# 3. Delete QnA
@router.delete("/{qna_id}")
def delete_qna(
    qna_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    qna = db.query(QnA).filter(QnA.qna_id == qna_id).first()
    if not qna:
        raise HTTPException(status_code=404, detail="QnA not found")
    db.delete(qna)
    db.commit()
    return {"message": "QnA deleted successfully"}

# 4. Answer a QnA
@router.patch("/{qna_id}/answer", response_model=QnAResponse)
def answer_qna(
    qna_id: int,
    data: QnAAnswerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    qna = db.query(QnA).filter(QnA.qna_id == qna_id).first()
    if not qna:
        raise HTTPException(status_code=404, detail="QnA not found")
    qna.answer = data.answer
    db.commit()
    db.refresh(qna)
    return qna
