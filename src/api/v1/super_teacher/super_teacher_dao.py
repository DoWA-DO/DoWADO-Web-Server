# super_teacher_dao.py

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

from src.api.v1.super_teacher.super_teacher_dto import ReadTeacherInfo, CreateTeacher, UpdateTeacher
from src.database.model import Teacher
from src.database.session import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Read
async def get_teacher(db: AsyncSession) -> list[ReadTeacherInfo]:  # = Depends(get_db)
    result = await db.execute(select(Teacher))
    teacher_info = result.scalars().all()
    return teacher_info

# Create
async def create_teacher(teacher: CreateTeacher, db: AsyncSession) -> None:
    '''
    if not await verify_email(teacher.teacher_email): 
        raise ValueError("Unauthorized to create a teacher") # 인증 실패
    '''
    db_user = Teacher(teacher_name=teacher.teacher_name,
                   teacher_password=pwd_context.hash(teacher.teacher_password),  # 해시화
                   teacher_auth=True,
                   teacher_email=teacher.teacher_email,
                   teacher_schoolname=teacher.teacher_schoolname)
    db.add(db_user)
    await db.commit()
    
async def get_existing_user(db: AsyncSession, teacher: CreateTeacher) -> Optional[Teacher]: # 중복 예외 처리
    query = select(Teacher).where(
        (Teacher.teacher_name == teacher.teacher_name) |
        (Teacher.teacher_email == teacher.teacher_email)
    )
    result = await db.execute(query)
    existing_teacher = result.scalars().first()
    return existing_teacher
        
# Update
async def update_teacher(teacher_email: str, teacher_info: UpdateTeacher, db: AsyncSession) -> None:
    await db.execute(update(Teacher).filter(Teacher.teacher_email==teacher_email).values(teacher_info.dict()))
    await db.commit()
    

# Delete
async def delete_teacher(teacher_email: str, db: AsyncSession) -> None:
    await db.execute(delete(Teacher).where(Teacher.teacher_email == teacher_email))
    await db.commit()

# Verify
async def verify_email(teacher_email: str) -> bool:

    # 이메일 확인 및 처리 로직
    try:
        # 이메일 확인 및 처리 로직 수행
        return {"message": "Account verified successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to verify account: {e}")

    
async def verify_teacher(teacher_email: str, db: AsyncSession) -> bool:
    """
    교사 계정 인증 함수
    
    Args:
        teacher_email (str): 인증할 교사 이메일
        db (AsyncSession): 데이터베이스 세션
    
    Returns:
        bool: 인증 성공 여부
    """
    try:
        # 데이터베이스에서 교사 정보 조회
        result = await db.execute(select(Teacher).filter(Teacher.teacher_email == teacher_email))
        teacher = result.scalar_one_or_none()
        
        if teacher:
            # 교사 계정이 이미 인증된 경우
            if teacher.teacher_auth:
                return True
            else:
                # 교사 계정 인증 로직 수행
                # 예: 이메일 인증 코드 발송 및 확인, 관리자 승인 등
                await update_teacher(teacher_email, UpdateTeacher(teacher_auth=True), db)
                return True
        else:
            # 교사 계정이 존재하지 않는 경우
            return False
    except Exception as e:
        # 인증 실패 시 예외 처리
        raise HTTPException(status_code=500, detail=f"Failed to verify teacher account: {e}")


