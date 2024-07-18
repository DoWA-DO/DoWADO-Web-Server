# teacher_dao.py

"""
API 개발 시 참고 : 비즈니스 로직 작성, service에서 호출
"""
# 기본적으로 추가

import logging
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.users.teacher.teacher_dto import ReadTeacherInfo, CreateTeacher, UpdateTeacher
from src.database.model import UserTeacher
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)

# Read
async def get_teacher(username: str, db: AsyncSession) -> ReadTeacherInfo:  
    logger.info(f"해당 계정이 연결됨 -> {username}")
    result = await db.execute(select(UserTeacher).where(UserTeacher.teacher_email == username))
    teacher_info = result.scalars().first()
    logger.info(teacher_info)
    return teacher_info

# Create
async def create_teacher(teacher: CreateTeacher, db: AsyncSession) -> None:
    db_user = UserTeacher(teacher_name=teacher.teacher_name,
                   teacher_password=pwd_context.hash(teacher.teacher_password),  # 해시화
                   teacher_email=teacher.teacher_email,
                   teacher_school=teacher.teacher_school,
                   teacher_grade=teacher.teacher_grade,
                   teacher_class=teacher.teacher_class,
                   )
    db.add(db_user)
    await db.commit()
    
async def get_existing_user(db: AsyncSession, teacher: CreateTeacher) -> Optional[UserTeacher]: # 중복 예외 처리
    query = select(UserTeacher).where(
        (UserTeacher.teacher_name == teacher.teacher_name) |
        (UserTeacher.teacher_email == teacher.teacher_email)
    )
    result = await db.execute(query)
    existing_teacher = result.scalars().first()
    return existing_teacher
        
# Update
async def update_teacher(teacher_email: str, teacher_info: UpdateTeacher, db: AsyncSession) -> None:
    
    # 기존 비밀번호 해시 값 가져오기
    existing_teacher = await db.get(UserTeacher, teacher_email)
    
    # 새 비밀번호 해시화
    new_password_hash = pwd_context.hash(teacher_info.teacher_password)
    
    # 비밀번호 해시 값 업데이트
    existing_teacher.teacher_password = new_password_hash

    await db.commit()
    
'''
# Delete
async def delete_teacher(teacher_email: str, db: AsyncSession) -> None:
    await db.execute(delete(UserTeacher).where(UserTeacher.teacher_email == teacher_email))
    await db.commit()
'''