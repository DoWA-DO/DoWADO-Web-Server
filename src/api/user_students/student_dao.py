# student_dao.py

"""
API 개발 시 참고 : 비즈니스 로직 작성, service에서 호출
"""
# 기본적으로 추가

import logging
from typing import Optional
from fastapi import HTTPException
from sqlalchemy import select, update, delete
# from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import AsyncSession, rdb
from src.api.user_students.student_dto import ReadStudentInfo, CreateStudent, UpdateStudent
from src.database.models import UserStudent
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)

# Read
@rdb.dao()
async def get_student(username: str, db: AsyncSession = rdb.inject_async()) -> ReadStudentInfo:  
    logger.info(f"해당 계정이 연결됨 -> {username}")
    result = await db.execute(select(UserStudent).where(UserStudent.student_email == username))
    student_info = result.scalars().first()
    logger.info(student_info)
    return student_info

# Create
@rdb.dao()
async def create_student(student: CreateStudent, db: AsyncSession = rdb.inject_async()) -> None:

    db_user = UserStudent(student_name=student.student_name,
                   student_password=pwd_context.hash(student.student_password),  # 해시화
                   student_email=student.student_email,
                   student_school=student.student_school,
                   student_grade=student.student_grade,
                   student_class=student.student_class,
                   student_number=student.student_number,
                   student_teacher_email=student.student_teacher_email
                   )
    db.add(db_user)
    await db.commit()
        
# Update
@rdb.dao()
async def update_student(student_info: UpdateStudent, username: str, db: AsyncSession = rdb.inject_async()) -> None:
    # 기존 비밀번호 해시 값 가져오기
    existing_student = await db.get(UserStudent, username)
    logger.info(existing_student)
    
    # 현재 비밀번호 db와 비교
    if not pwd_context.verify(student_info.student_password, existing_student.student_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 새 비밀번호 해시화
    new_password_hash = pwd_context.hash(student_info.new_password)
    # 비밀번호 해시 값 업데이트
    existing_student.student_password = new_password_hash
    await db.commit()
    
'''
# Delete
async def delete_student(student_email: str, db: AsyncSession) -> None:
    await db.execute(delete(UserStudent).where(UserStudent.student_email == student_email))
    await db.commit()'''