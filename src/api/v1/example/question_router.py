from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from src.database.session import SessionLocal,get_db
from src.database.model import Job

router = APIRouter(
    prefix="/question",
)

@router.get("/list", response_model=list[Job]) # Job 스키마
def question_list(db: Session = Depends(get_db)):
    _question_list = db.query(Job).order_by(Job.create_date.desc()).all()
    return _question_list