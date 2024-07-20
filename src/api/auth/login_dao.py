"""
NOTE: 리펙토링 작업 전
"""
import logging
from sqlalchemy import select 
from src.database.models import UserTeacher, UserStudent
from src.database.session import AsyncSession, rdb


@rdb.dao()
async def get_student_user(username: str, db: AsyncSession = rdb.inject_async()):
    student_result = await db.execute(select(UserStudent).filter(UserStudent.student_email == username).limit(1))
    student = student_result.scalars().first()
    if student:
        logging.info(f"Student info: {student.student_email, student.student_password}")
        return student.student_password, student.student_email
    else:
        return None, None

@rdb.dao()
async def get_teacher_user(username: str, db: AsyncSession = rdb.inject_async()):
    teacher_result = await db.execute(select(UserTeacher).filter(UserTeacher.teacher_email == username).limit(1))
    teacher = teacher_result.scalars().first()
    if teacher:
        logging.info(f"Teacher info: {teacher.teacher_email, teacher.teacher_password}")
        return teacher.teacher_password, teacher.teacher_email
    else:
        return None, None
    
