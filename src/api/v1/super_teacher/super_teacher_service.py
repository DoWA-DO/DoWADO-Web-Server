# super_tecaher_service.py

"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 호출할 모듈 추가
from src.api.v1.super_teacher.super_teacher_dto import ReadTeacherInfo, CreateTeacher, UpdateTeacher
from src.api.v1.super_teacher import super_teacher_dao

# 이후 삭제 예정, 일단 기본 추가
from sqlalchemy.ext.asyncio import AsyncSession


# Read
async def get_teacher(db: AsyncSession) -> list[ReadTeacherInfo]:
    teacher_info = await super_teacher_dao.get_teacher(db)
    return teacher_info

# Create
async def create_teacher(teacher: CreateTeacher, db: AsyncSession) -> None:
    await super_teacher_dao.create_teacher(teacher, db)
    
    
# Update
async def update_teacher(teacher_email: str, teacher_info: UpdateTeacher, db: AsyncSession) -> None:
    await super_teacher_dao.update_teacher(teacher_email, teacher_info, db)
    

# Delete
async def delete_teacher(teacher_email: str, db: AsyncSession) -> None:
    await super_teacher_dao.delete_teacher(teacher_email, db)