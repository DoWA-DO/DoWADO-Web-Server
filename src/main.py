from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from src.database.model import Base, Job
from src.database.session import engine, SessionLocal, get_db
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()
Base.metadata.create_all(bind=engine)

class CreateJobRequest(BaseModel):
    title: str
    description: str
    created_at: datetime = None
    updated_at: datetime = None

@app.post("/jobs")
def create_job(details: CreateJobRequest, db: Session = Depends(get_db)):
    try:
        to_create = Job(
            title=details.title,
            description=details.description,
            created_at=details.created_at or datetime.now(),
            updated_at=details.updated_at or datetime.now()
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

@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

@app.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    try:
        deleted_job = db.query(Job).filter(Job.id == job_id).first()
        if not deleted_job:
            raise HTTPException(status_code=404, detail="Job not found")
        db.delete(deleted_job)
        db.commit()
        return {"deleted_id": deleted_job.id}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
