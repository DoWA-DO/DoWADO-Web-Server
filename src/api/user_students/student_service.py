from typing import Union
from src.api.user_students.student_dto import ReadStudentInfo, CreateStudent, UpdateStudent
from src.api.user_students import student_dao

async def get_student(username: str) -> Union[ReadStudentInfo, None]:
    student_info = await student_dao.get_student(username)
    return student_info

async def create_student(student: CreateStudent) -> None:
    await student_dao.create_student(student)
    
async def update_student(username: str, student_info: UpdateStudent) -> None:
    await student_dao.update_student(username, student_info)
