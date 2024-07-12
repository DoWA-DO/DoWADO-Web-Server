# login_dao.py

"""
API 개발 시 참고 : 비즈니스 로직 작성, service에서 호출
"""
# 기본적으로 추가
import logging
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.model import UserTeacher, UserStudent

async def get_user(db: AsyncSession, username: str):
    """
    Fetch the user from the database and return the user's password, email, and user type.
    """
    teacher_result = await db.execute(select(UserTeacher).filter(UserTeacher.teacher_email == username).limit(1))
    teacher = teacher_result.scalars().first()

    if teacher:
        logging.info(f"Teacher info: {teacher.teacher_email, teacher.teacher_password}")
        return teacher.teacher_password, teacher.teacher_email, "teacher"

    student_result = await db.execute(select(UserStudent).filter(UserStudent.student_email == username).limit(1))
    student = student_result.scalars().first()

    if student:
        logging.info(f"Student info: {student.student_email, student.student_password}")
        return student.student_password, student.student_email, "student"

    return None, None, None
