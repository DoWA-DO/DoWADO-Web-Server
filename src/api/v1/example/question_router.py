from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.database.model import Job
from src.api.v1.example import question_crud

router = APIRouter(
    prefix="/question",
)

@router.get("/list", response_model=list[Job]) # Job 스키마
def question_list(db: Session = Depends(get_db)):
    _question_list = question_crud.get_question_list(db)
    return _question_list