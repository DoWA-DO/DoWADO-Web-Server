# teacher_dao.py

"""
API 개발 시 참고 : 비즈니스 로직 작성, service에서 호출
"""
# 기본적으로 추가

import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import AsyncSession, rdb
from src.api.user_teachers.teacher_dto import ReadTeacherInfo, CreateTeacher, UpdateTeacher
from src.database.models import UserTeacher
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)

# Read
@rdb.dao()
async def get_teacher(username: str, session: AsyncSession = rdb.inject_async()) -> ReadTeacherInfo:  
    logger.info(f"해당 계정이 연결됨 -> {username}")
    result = await session.execute(select(UserTeacher).where(UserTeacher.teacher_email == username))
    teacher_info = result.scalars().first()
    logger.info(teacher_info)
    return teacher_info

# Create
@rdb.dao()
async def create_teacher(teacher: CreateTeacher, session: AsyncSession = rdb.inject_async()) -> None:
    db_user = UserTeacher(teacher_name=teacher.teacher_name,
                   teacher_password=pwd_context.hash(teacher.teacher_password),  # 해시화
                   teacher_email=teacher.teacher_email,
                   teacher_school=teacher.teacher_school,
                   teacher_grade=teacher.teacher_grade,
                   teacher_class=teacher.teacher_class,
                   )
    session.add(db_user)
    await session.commit()
        
# Update
@rdb.dao()
async def update_teacher(teacher_info: UpdateTeacher, username: str, session: AsyncSession = rdb.inject_async()) -> None:
    
    # 기존 비밀번호 해시 값 가져오기
    existing_teacher = await session.get(UserTeacher, username)
    logger.info(existing_teacher)
    
    # 현재 비밀번호 db와 비교
    if not pwd_context.verify(teacher_info.teacher_password, existing_teacher.teacher_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 새 비밀번호 해시화
    new_password_hash = pwd_context.hash(teacher_info.new_password)
    
    # 비밀번호 해시 값 업데이트
    existing_teacher.teacher_password = new_password_hash
    await session.commit()
    
'''
# Delete
async def delete_teacher(teacher_email: str, db: AsyncSession) -> None:
    await db.execute(delete(UserTeacher).where(UserTeacher.teacher_email == teacher_email))
    await db.commit()
'''