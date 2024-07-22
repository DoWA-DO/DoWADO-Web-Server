from src.api.user_teachers.teacher_dao import get_teacher, create_teacher, save_verification_code, verify_email
from src.api.user_teachers.teacher_dto import ReadTeacherInfo, CreateTeacher, UpdateTeacher
from fastapi import HTTPException

async def get_teacher_info(email: str) -> ReadTeacherInfo:
    teacher_info = await get_teacher(email)
    if not teacher_info:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return ReadTeacherInfo(
        school_id=teacher_info.school_id,
        teacher_name=teacher_info.teacher_name,
        teacher_email=teacher_info.teacher_email,
        teacher_grade=teacher_info.teacher_grade,
        teacher_class=teacher_info.teacher_class,
        is_verified=teacher_info.is_verified
    )

async def create_teacher_service(teacher: CreateTeacher) -> None:
    if await get_teacher(teacher.teacher_email):
        raise HTTPException(status_code=409, detail="Duplicate email")
    await create_teacher(teacher)

async def save_verification_code_service(email: str, code: str) -> None:
    await save_verification_code(email, code)

async def verify_email_service(email: str, code: str) -> None:
    await verify_email(email, code)
