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

from src.database.model import UserTeacher
from src.database.session import get_db
from passlib.context import CryptContext

async def get_user(db: AsyncSession, username: str):
    """
    Fetch the user from the database and return the teacher password.
    """
    result = await db.execute(select(UserTeacher).filter(UserTeacher.teacher_email == username).limit(1))
    user = result.scalars().first()
    #hashed_password = [teacher.teacher_password for teacher in user]
    
    if user:
        logging.info(f"Teacher info: {user.teacher_email, user.teacher_password}")
        return user.teacher_password, user.teacher_email
    else:
        return None, None