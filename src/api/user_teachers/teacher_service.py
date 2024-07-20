from typing import Union
from src.api.user_teachers.teacher_dto import ReadTeacherInfo, CreateTeacher, UpdateTeacher
from src.api.user_teachers import teacher_dao

async def get_teacher(username: str) -> Union[ReadTeacherInfo, None]:
    teacher_info = await teacher_dao.get_teacher(username)
    return teacher_info

async def create_teacher(teacher: CreateTeacher) -> None:
    await teacher_dao.create_teacher(teacher)
    
async def update_teacher(username: str, teacher_info: UpdateTeacher) -> None:
    await teacher_dao.update_teacher(username, teacher_info)
