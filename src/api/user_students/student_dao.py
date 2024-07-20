from typing import Optional
from fastapi import HTTPException
from sqlalchemy import select, update, delete
from src.database.session import AsyncSession, rdb
from src.api.user_students.student_dto import ReadStudentInfo, CreateStudent, UpdateStudent
from src.database.models import UserStudent
from passlib.context import CryptContext
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)

@rdb.dao()
async def get_student(username: str, session: AsyncSession = rdb.inject_async()) -> ReadStudentInfo:  
    logger.info(f"해당 계정이 연결됨 -> {username}")
    result = await session.execute(select(UserStudent).where(UserStudent.student_email == username))
    student_info = result.scalars().first()
    logger.info(student_info)
    return student_info

@rdb.dao()
async def create_student(student: CreateStudent, session: AsyncSession = rdb.inject_async()) -> None:
    db_user = UserStudent(
        student_name=student.student_name,
        student_password=pwd_context.hash(student.student_password),  # 해시화
        student_email=student.student_email,
        student_school=student.student_school,
        student_grade=student.student_grade,
        student_class=student.student_class,
        student_number=student.student_number
    )
    session.add(db_user)
    await session.commit()

@rdb.dao()
async def update_student(username: str, student_info: UpdateStudent, session: AsyncSession = rdb.inject_async()) -> None:
    existing_student = await session.execute(select(UserStudent).where(UserStudent.student_email == username))
    existing_student = existing_student.scalars().first()
    logger.info(existing_student)
    
    if not pwd_context.verify(student_info.student_password, existing_student.student_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    new_password_hash = pwd_context.hash(student_info.new_password)
    existing_student.student_password = new_password_hash
    await session.commit()
