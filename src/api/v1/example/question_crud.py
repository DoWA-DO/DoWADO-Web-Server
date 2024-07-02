from src.database.model import Job
from sqlalchemy.orm import Session
from sqlalchemy import select

""" 동기
def get_question_list(db: Session):
    question_list = db.query(Job)\
        .order_by(Job.create_date.desc())\
        .all()
    return question_list
"""

# 비동기
async def get_async_question_list(db: Session):
    data = await db.execute(select(Job)
                            .order_by(Job.create_date.desc())
                            .limit(10))
    return data.all()