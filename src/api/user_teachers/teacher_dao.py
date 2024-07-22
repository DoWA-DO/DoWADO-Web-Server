# from sqlalchemy import select
# from fastapi import HTTPException
# # from src.database.session import AsyncSessionLocal
# from src.database.session import AsyncSession, rdb
# from src.api.user_teachers.teacher_dto import CreateTeacher, UpdateTeacher
# from src.database.models import UserTeacher
# from passlib.context import CryptContext
# import logging


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# logger = logging.getLogger(__name__)

# @rdb.dao()
# async def get_teacher(email: str, session: AsyncSession = rdb.inject_async()) -> UserTeacher:
#     logger.info(f"해당 계정이 연결됨 -> {email}")
#     result = await session.execute(select(UserTeacher).where(UserTeacher.teacher_email == email))
#     teacher_info = result.scalars().first()
#     logger.info(teacher_info)
#     return teacher_info


# @rdb.dao()
# async def create_teacher(teacher: CreateTeacher, session: AsyncSession = rdb.inject_async()) -> None:
#     db_user = UserTeacher(
#         school_id=teacher.school_id,
#         teacher_grade=teacher.teacher_grade,
#         teacher_class=teacher.teacher_class,
#         teacher_email=teacher.teacher_email,
#         teacher_name=teacher.teacher_name,
#         teacher_password=pwd_context.hash(teacher.teacher_password),  # 해시화
#     )
#     session.add(db_user)
#     await session.commit()


# @rdb.dao()
# async def update_teacher(email: str, teacher_info: UpdateTeacher, session: AsyncSession = rdb.inject_async()) -> None:
#     existing_teacher = await session.execute(select(UserTeacher).where(UserTeacher.teacher_email == email))
#     existing_teacher = existing_teacher.scalars().first()
#     logger.info(existing_teacher)
    
#     if not pwd_context.verify(teacher_info.teacher_password, existing_teacher.teacher_password):
#         raise HTTPException(
#             status_code=401,
#             detail="Incorrect password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     new_password_hash = pwd_context.hash(teacher_info.new_password)
#     existing_teacher.teacher_password = new_password_hash
#     await session.commit()
    




# src/api/user_teachers/teacher_dao.py
from sqlalchemy import select, update
from fastapi import HTTPException
from src.database.session import AsyncSession, rdb
from src.api.user_teachers.teacher_dto import CreateTeacher, UpdateTeacher
from src.database.models import UserTeacher, EmailVerification
from passlib.context import CryptContext
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)

@rdb.dao()
async def get_teacher(email: str, session: AsyncSession = rdb.inject_async()) -> UserTeacher:
    logger.info(f"해당 계정이 연결됨 -> {email}")
    result = await session.execute(select(UserTeacher).where(UserTeacher.teacher_email == email))
    return result.scalars().first()

@rdb.dao()
async def create_teacher(teacher: CreateTeacher, session: AsyncSession = rdb.inject_async()) -> None:
    db_teacher = UserTeacher(
        school_id=teacher.school_id,
        teacher_grade=teacher.teacher_grade,
        teacher_class=teacher.teacher_class,
        teacher_email=teacher.teacher_email,
        teacher_name=teacher.teacher_name,
        teacher_password=pwd_context.hash(teacher.teacher_password),
        is_verified=False  # 기본값으로 인증되지 않은 상태로 설정
    )
    session.add(db_teacher)
    await session.commit()

@rdb.dao()
async def save_verification_code(email: str, code: str, session: AsyncSession = rdb.inject_async()) -> None:
    db_verification = EmailVerification(
        email=email,
        verification_code=code
    )
    session.add(db_verification)
    await session.commit()

@rdb.dao()
async def verify_email(email: str, code: str, session: AsyncSession = rdb.inject_async()) -> None:
    result = await session.execute(select(EmailVerification).where(EmailVerification.email == email))
    verification = result.scalars().first()
    if verification and verification.verification_code == code:
        await session.execute(update(UserTeacher).where(UserTeacher.teacher_email == email).values(is_verified=True))
        await session.commit()
    else:
        raise HTTPException(status_code=400, detail="Invalid verification code")
