# login_dao.py

"""
API 개발 시 참고 : 비즈니스 로직 작성, service에서 호출
"""
# 기본적으로 추가
import logging
from typing import Optional
from fastapi import Depends, HTTPException
from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload, query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.model import UserTeacher, UserStudent
from src.database.session import get_db
from passlib.context import CryptContext

async def get_user(db: AsyncSession, username: str):
    """
    Fetch the user from the database and return the teacher or student password.
    """
    teacher_result = await db.execute(select(UserTeacher).filter(UserTeacher.teacher_email == username).limit(1))
    teacher = teacher_result.scalars().first()

    student_result = await db.execute(select(UserStudent).filter(UserStudent.student_email == username).limit(1))
    student = student_result.scalars().first()

    if teacher:
        logging.info(f"Teacher info: {teacher.teacher_email, teacher.teacher_password}")
        return teacher.teacher_password, teacher.teacher_email, "teacher"
    elif student:
        logging.info(f"Student info: {student.student_email, student.student_password}")
        return student.student_password, student.student_email, "student"
    else:
        return None, None, None