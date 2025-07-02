from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.qna import QnA
from models.user import User
from schemas.qna import QnAResponse, QnAStatusUpdate, QnAAnswerUpdate
from dependencies.admin_dependency import admin_required

router = APIRouter(prefix="/api/admin/qna", tags=["Admin QnA"])

# 1. Get all QnAs without Pagination
@router.get("/", response_model=list[QnAResponse])
def get_all_qnas(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    qnas = db.query(QnA).all()  # Fetch all QnA data
    return qnas
@router.patch("/{qna_id}/status", response_model=QnAResponse)
def update_qna_status(
    qna_id: int,
    data: QnAStatusUpdate,  # This should be the correct schema
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    print("Received data:", data)  # Debugging: log incoming data
    qna = db.query(QnA).filter(QnA.qna_id == qna_id).first()
    if not qna:
        raise HTTPException(status_code=404, detail="QnA not found")
    
    print(f"Before Update: is_public = {qna.is_public}")  # Debugging: log QnA before update
    
    qna.is_public = data.is_public  # Update the is_public field
    db.commit()  # Commit changes to the database
    db.refresh(qna)  # Refresh to ensure updated values are reflected

    print(f"After Update: is_public = {qna.is_public}")  # Debugging: log QnA after update
    
    return qna  # Return the updated QnA object



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

@router.patch("/{qna_id}/answer", response_model=QnAResponse)
def answer_qna(
    qna_id: int,
    data: QnAAnswerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    # Fetch the QnA entry from the database
    qna = db.query(QnA).filter(QnA.qna_id == qna_id).first()
    if not qna:
        raise HTTPException(status_code=404, detail="QnA not found")
    # Check if is_public is false, and set it to true
    if not qna.is_public:
        qna.is_public = True
    # Update the answer
    qna.answer = data.answer
    # Commit the changes to the database
    db.commit()
    # Refresh the QnA object to get the updated values
    db.refresh(qna)
    # Return the updated QnA object
    return qna

