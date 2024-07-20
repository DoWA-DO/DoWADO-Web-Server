from typing import Optional
from fastapi import HTTPException
from sqlalchemy import select, update, delete
from src.database.session import AsyncSession, rdb
from src.api.user_teachers.teacher_dto import ReadTeacherInfo, CreateTeacher, UpdateTeacher
from src.database.models import UserTeacher
from passlib.context import CryptContext
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)

@rdb.dao()
async def get_teacher(username: str, session: AsyncSession = rdb.inject_async()) -> ReadTeacherInfo:  
    logger.info(f"해당 계정이 연결됨 -> {username}")
    result = await session.execute(select(UserTeacher).where(UserTeacher.teacher_email == username))
    teacher_info = result.scalars().first()
    logger.info(teacher_info)
    return teacher_info

@rdb.dao()
async def create_teacher(teacher: CreateTeacher, session: AsyncSession = rdb.inject_async()) -> None:
    db_user = UserTeacher(
        teacher_name=teacher.teacher_name,
        teacher_password=pwd_context.hash(teacher.teacher_password),  # 해시화
        teacher_email=teacher.teacher_email,
        teacher_school=teacher.teacher_school,
        teacher_grade=teacher.teacher_grade,
        teacher_class=teacher.teacher_class
    )
    session.add(db_user)
    await session.commit()

@rdb.dao()
async def update_teacher(username: str, teacher_info: UpdateTeacher, session: AsyncSession = rdb.inject_async()) -> None:
    existing_teacher = await session.execute(select(UserTeacher).where(UserTeacher.teacher_email == username))
    existing_teacher = existing_teacher.scalars().first()
    logger.info(existing_teacher)
    
    if not pwd_context.verify(teacher_info.teacher_password, existing_teacher.teacher_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    new_password_hash = pwd_context.hash(teacher_info.new_password)
    existing_teacher.teacher_password = new_password_hash
    await session.commit()
