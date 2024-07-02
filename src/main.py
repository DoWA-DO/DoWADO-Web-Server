from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from src.database.model import Base, Job
from src.database.session import engine, SessionLocal, get_db
from sqlalchemy.exc import SQLAlchemyError
from src.api.v1.example import question_router

app = FastAPI()
Base.metadata.create_all(bind=engine)

class CreateJobRequest(BaseModel):
    subject: str
    content: str
    create_date: datetime = None
    
class JobResponse(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime

@app.post("/jobs")
def create_job(details: CreateJobRequest, db: Session = Depends(get_db)):
    try:
        to_create = Job(
            subject=details.subject,
            content=details.content,
            create_date=details.create_date or datetime.now()
        )
        db.add(to_create)
        db.commit()
        db.refresh(to_create)
        return to_create
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs", response_model=list[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    try:
        jobs = db.query(Job).all()
        return jobs
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(question_router.router) # router 객체 등록