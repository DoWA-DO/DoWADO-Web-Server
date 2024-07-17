# su_dao.py

"""
API 개발 시 참고 : 비즈니스 로직 작성, service에서 호출
"""
# 기본적으로 추가

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.users.signup.su_dto import CreateTeacher, UpdateTeacher, UserStudent, CreateStudent

from src.database.model import UserTeacher, UserStudent
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create teacher
async def create_teacher(teacher: CreateTeacher, db: AsyncSession) -> None:
    '''
    if not await verify_email(teacher.teacher_email): 
        raise ValueError("Unauthorized to create a teacher") # 인증 실패
    '''
    db_user = UserTeacher(teacher_name=teacher.teacher_name,
                   teacher_password=pwd_context.hash(teacher.teacher_password),  # 해시화
                   teacher_email=teacher.teacher_email,
                   teacher_school=teacher.teacher_school,
                   teacher_grade=teacher.teacher_grade,
                   teacher_class=teacher.teacher_class,
                   )
    db.add(db_user)
    await db.commit()

async def create_student(student: CreateStudent, db: AsyncSession) -> None:
    '''
    if not await verify_email(teacher.teacher_email): 
        raise ValueError("Unauthorized to create a teacher") # 인증 실패
    '''
    db_user = UserStudent(student_name=student.student_name,
                   student_password=pwd_context.hash(student.student_password),  # 해시화
                   student_email=student.student_email,
                   student_school=student.student_school,
                   student_grade=student.student_grade,
                   student_class=student.student_class,
                   student_number=student.student_number,
                   student_teacher_email=student.student_teacher_email
                   )
    db.add(db_user)
    await db.commit()
    
async def get_existing_teacher(db: AsyncSession, teacher: CreateTeacher) -> Optional[UserTeacher]: # 중복 예외 처리
    query = select(UserTeacher).where(
        (UserTeacher.teacher_name == teacher.teacher_name) |
        (UserTeacher.teacher_email == teacher.teacher_email)
    )
    result = await db.execute(query)
    existing_teacher = result.scalars().first()
    return existing_teacher
    
async def get_existing_student(db: AsyncSession, student: CreateStudent) -> Optional[UserStudent]: # 중복 예외 처리
    query = select(UserStudent).where(
        (UserStudent.student_name == student.student_name) |
        (UserStudent.student_email == student.student_email)
    )
    result = await db.execute(query)
    existing_student = result.scalars().first()
    return existing_student


# Update teacher
async def update_teacher(teacher_email: str, teacher_info: UpdateTeacher, db: AsyncSession) -> None:
    
    # 기존 비밀번호 해시 값 가져오기
    existing_teacher = await db.get(UserTeacher, teacher_email)
    
    # 새 비밀번호 해시화
    new_password_hash = pwd_context.hash(teacher_info.teacher_password)
    
    # 비밀번호 해시 값 업데이트
    existing_teacher.teacher_password = new_password_hash

    await db.commit()   

# Update student
async def update_student(student_email: str, student_info: UpdateStudent, db: AsyncSession) -> None:
    # 기존 비밀번호 해시 값 가져오기
    existing_teacher = await db.get(UserStudent, student_email)
    
    # 새 비밀번호 해시화
    new_password_hash = pwd_context.hash(student_info.teacher_password)
    
    # 비밀번호 해시 값 업데이트
    existing_teacher.teacher_password = new_password_hash

    await db.commit()
    await db.commit()