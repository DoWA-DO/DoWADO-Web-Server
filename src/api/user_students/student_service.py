from src.api.user_students.student_dto import ReadStudentInfo, CreateStudent, UpdateStudent
from src.api.user_students import student_dao
from fastapi import HTTPException
from src.config.status import ER
from src.config.security import Crypto


async def get_student(email: str) -> ReadStudentInfo:
    student_info = await student_dao.get_student(email)
    if not student_info:
        raise HTTPException(status_code=404, detail="Student not found")
    return ReadStudentInfo(
        school_id=student_info.school_id,
        student_name=student_info.student_name,
        student_email=student_info.student_email,
        student_grade=student_info.student_grade,
        student_class=student_info.student_class,
        student_number=student_info.student_number
    )

async def create_student(student: CreateStudent) -> None:
    if await student_dao.check_duplicate_email(student.student_email):
        raise HTTPException(status_code=409, detail="Duplicate email")
    await student_dao.create_student(student)
    
    
async def update_student(email: str, student_info: UpdateStudent) -> None:
    await student_dao.update_student(email, student_info)