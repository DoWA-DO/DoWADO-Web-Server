# tecaher_service.py

"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 호출할 모듈 추가
from typing import Optional, Union
from src.api.v1.users.teacher.teacher_dto import ReadTeacherInfo, CreateTeacher, UpdateTeacher
from src.api.v1.users.teacher import teacher_dao

# 이후 삭제 예정, 일단 기본 추가
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.model import UserTeacher


# Read
async def get_teacher(username: str, db: AsyncSession) -> Union[ReadTeacherInfo, None]:
    teacher_info = await teacher_dao.get_teacher(username, db)
    return teacher_info

# Create
async def create_teacher(teacher: CreateTeacher, db: AsyncSession) -> None:
    await teacher_dao.create_teacher(teacher, db)
    
    
# Update
async def update_teacher(teacher_email: str, teacher_info: UpdateTeacher, db: AsyncSession) -> None:
    await teacher_dao.update_teacher(teacher_email, teacher_info, db)
    
'''
# Delete
async def delete_teacher(teacher_email: str, db: AsyncSession) -> None:
    await teacher_dao.delete_teacher(teacher_email, db)
'''