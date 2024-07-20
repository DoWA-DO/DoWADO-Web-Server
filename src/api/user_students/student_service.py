# student_service.py

"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 호출할 모듈 추가
from typing import Union
from src.api.user_students.student_dto import ReadStudentInfo, CreateStudent, UpdateStudent
from src.api.user_students import student_dao

# # 이후 삭제 예정, 일단 기본 추가
# from sqlalchemy.ext.asyncio import AsyncSession


# Read
async def get_student(username: str) -> Union[ReadStudentInfo, None]:
    student_info = await student_dao.get_student(username)
    return student_info

# Create
async def create_student(student: CreateStudent) -> None:
    await student_dao.create_student(student)
    
    
# Update
async def update_student(student_email: str, student_info: UpdateStudent) -> None:
    await student_dao.update_student(student_email, student_info)
    
'''
# Delete
async def delete_student(student_email: str, db: AsyncSession) -> None:
    await student_dao.delete_student(student_email, db)
'''