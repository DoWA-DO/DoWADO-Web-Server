from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import NoResultFound
from src.database.models import UserTeacher, UserStudent, School
from src.config.status import ER
from src.database.session import AsyncSession, rdb
from fastapi import HTTPException
import logging


logger = logging.getLogger(__name__)

@rdb.dao()
async def get_teacher(email: str, session: AsyncSession = rdb.inject_async()) -> UserTeacher:
    """
    이메일을 통해 교사 정보를 데이터베이스에서 가져오는 함수.
    
    :param email: 교사의 이메일 주소
    :param session: 데이터베이스 세션 객체 (디폴트로 주입됨)
    :return: UserTeacher 객체
    :raises NoResultFound: 교사를 찾지 못한 경우
    """
    try:
        logger.info(f"Fetching teacher with email: {email}")
        result = await session.execute(select(UserTeacher).where(UserTeacher.teacher_email == email))
        user = result.scalar_one_or_none()
        if user is None:
            logger.error(f"No teacher found for email: {email}")
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        logger.error(f"Error retrieving teacher: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from None



@rdb.dao()
async def get_student(email: str, session: AsyncSession = rdb.inject_async()) -> UserStudent:
    """
    이메일을 통해 학생 정보를 데이터베이스에서 가져오는 함수.
    
    :param email: 학생의 이메일 주소
    :param session: 데이터베이스 세션 객체 (디폴트로 주입됨)
    :return: UserStudent 객체
    :raises NoResultFound: 학생을 찾지 못한 경우
    """
    # try:
    #     result: Result = await session.execute(
    #         select(UserStudent).filter_by(student_email=email)
    #     )
    #     return result.scalar_one()
    # except NoResultFound:
    #     logger.error(f"No user found for email: {email}")
    #     raise HTTPException(status_code=404, detail="User not found") from None
    # except Exception as e:
    #     logger.error(f"Error retrieving user: {e}")
    #     raise HTTPException(status_code=500, detail="Internal Server Error") from None
    try:
        logger.info(f"Fetching student with email: {email}")
        result = await session.execute(select(UserStudent).where(UserStudent.student_email == email))
        user = result.scalar_one_or_none()
        if user is None:
            logger.error(f"No student found for email: {email}")
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        logger.error(f"Error retrieving student: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from None



@rdb.dao()
async def get_teacher_role(school_id: int, email: str, session: AsyncSession = rdb.inject_async()) -> UserTeacher:
    """
    학교 ID와 이메일을 통해 교사의 역할을 데이터베이스에서 가져오는 함수.
    
    :param school_id: 학교의 ID
    :param email: 교사의 이메일 주소
    :param session: 데이터베이스 세션 객체 (디폴트로 주입됨)
    :return: UserTeacher 객체
    :raises NoResultFound: 교사의 역할을 찾지 못한 경우
    """
    try:
        result: Result = await session.execute(
            select(UserTeacher).filter_by(school_id=school_id, teacher_email=email)
        )
        return result.scalar_one()
    except NoResultFound as err:
        raise ER.NOT_FOUND from err




@rdb.dao()
async def get_student_role(school_id: int, email: str, session: AsyncSession = rdb.inject_async()) -> UserStudent:
    """
    학교 ID와 이메일을 통해 학생의 역할을 데이터베이스에서 가져오는 함수.
    
    :param school_id: 학교의 ID
    :param email: 학생의 이메일 주소
    :param session: 데이터베이스 세션 객체 (디폴트로 주입됨)
    :return: UserStudent 객체
    :raises NoResultFound: 학생의 역할을 찾지 못한 경우
    """
    try:
        result: Result = await session.execute(
            select(UserStudent).filter_by(school_id=school_id, student_email=email)
        )
        return result.scalar_one()
    except NoResultFound as err:
        raise ER.NOT_FOUND from err


