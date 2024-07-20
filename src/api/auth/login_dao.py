from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import NoResultFound
from src.database.models import UserTeacher, UserStudent
from src.database.session import AsyncSession, rdb
from src.config.status import ER
import logging

logger = logging.getLogger(__name__)

@rdb.dao()
async def get_student_user(username: str, session: AsyncSession = rdb.inject_async()) -> UserStudent:
    ''' 주어진 이메일(username)을 가진 학생(UserStudent) 정보를 데이터베이스에서 가져옴 '''
    try:
        student_result: Result = await session.execute(select(UserStudent).filter_by(student_email=username))
        return student_result.scalar_one()
    # 예외 - 학생 정보를 찾을 수 없음.
    except NoResultFound as err: 
        raise ER.NOT_FOUND from err

@rdb.dao()
async def get_teacher_user(username: str, session: AsyncSession = rdb.inject_async()) -> UserTeacher:
    ''' 주어진 이메일(username)을 가진 교사(UserTeacher) 정보를 데이터베이스에서 가져옴 '''
    try:
        teacher_result: Result = await session.execute(select(UserTeacher).filter_by(teacher_email=username))
        return teacher_result.scalar_one()
    # 예외 - 교사 정보를 찾을 수 없음
    except NoResultFound as err:
        raise ER.NOT_FOUND from err
