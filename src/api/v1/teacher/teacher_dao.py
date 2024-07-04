"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 기본적으로 추가
from fastapi import Depends
from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload, query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.teacher.teacher_dto import ReadTeacherInfo, CreateTeacher, UpdateTeacher, keyTeacher
from src.database.models import Teacher
from src.database.session import get_db


# Read
async def get_teacher(db: AsyncSession) -> list[ReadTeacherInfo]:  # = Depends(get_db)
    result = await db.execute(select(Teacher))
    teacher_info = result.scalars().all()
    return teacher_info


# Create
async def create_teacher(teacher: CreateTeacher, db: AsyncSession) -> None:
    await db.execute(insert(Teacher).values(teacher.dict()))
    await db.commit() # 자동으로 commit되게 설정 변경 필요 
    
    
# Update
async def update_teacher(teacher_email: str, teacher_info: UpdateTeacher, db: AsyncSession) -> None:
    await db.execute(update(Teacher).filter(Teacher.teacher_email==teacher_email).values(teacher_info.dict()))
    await db.commit()
    

# Delete, 교원 삭제 부분은 super_teacher 로 넘어가 야함. - TODO
async def delete_teacher(teacher_email: str, db: AsyncSession) -> None:
    await db.execute(delete(Teacher).where(Teacher.teacher_email == teacher_email))
    await db.commit()