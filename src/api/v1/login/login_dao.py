# login_dao.py

"""
API 개발 시 참고 : 비즈니스 로직 작성, service에서 호출
"""
# 기본적으로 추가
import logging
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.model import UserTeacher, UserStudent
from src.api.v1.users.student.student_dao import get_student
from src.api.v1.users.teacher.teacher_dao import get_teacher

async def get_user(db: AsyncSession, username: str):
    """
    사용자 정보 조회
    """
    # 학생 정보 조회
    student = await get_student(db, username)
    if student:
        return (student.hashed_password, student.email)

    # 선생님 정보 조회
    teacher = await get_teacher(db, username)
    if teacher:
        return (teacher.hashed_password, teacher.email)

    return None
