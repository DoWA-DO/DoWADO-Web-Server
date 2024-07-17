# su_control.py

"""
API 개발 시 참고 : 프론트엔드에서 http 엔드포인트를 통해 호출되는 메서드
"""
# 기본적으로 추가
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from src.core.status import Status, SU, ER
import logging

# (db 세션 관련)이후 삭제 예정, 개발을 위해 일단 임시로 추가
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.core.config import SECRET_KEY
# 호출할 모듈 추가
from src.api.v1.signup.su_dto import ReadTeacherInfo, CreateTeacher, UpdateTeacher, CreateStudent
from src.api.v1.signup.su_dao import get_existing_teacher, get_existing_student
from src.api.v1.signup import su_service
from src.api.v1.users.teacher.teacher_dao import pwd_context

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
# secret key 생성 : openssl rand -hex 32
ALGORITHM = "HS256"

# 로깅 및 라우터 객체 생성 - 기본적으로 추가
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/signup", tags=["회원가입"])

STUDENT_SCOPE = "student"
TEACHER_SCOPE = "teacher"

# Create
@router.post(
    "/signup",
    summary="회원가입",
    description="- String-Form / Boolean-Form / String-Form / String-Form / String-Form",
    # response_model=ResultType, # -> 코드 미완성, 주석처리
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
if scope == STUDENT_SCOPE:
    async def create_teacher(
        teacher: Optional[CreateTeacher],
        db: AsyncSession = Depends(get_db)
    ):
        logger.info("----------신규 교원 생성----------")
    
        # 중복 여부 확인
        existing_teacher = await get_existing_teacher(db, teacher)
        if existing_teacher:
            raise HTTPException(status_code=409, detail=ER.DUPLICATE_RECORD)
    
        await su_service.create_teacher(teacher, db)
        return SU.CREATED
elif scope == TEACHER_SCOPE:
    async def create_student(
        student: Optional[CreateStudent],
        db: AsyncSession = Depends(get_db)
    ):
        logger.info("----------신규 학생 생성----------")
    
        # 중복 여부 확인
        existing_student = await get_existing_student(db, student)
        if existing_student:
            raise HTTPException(status_code=409, detail=ER.DUPLICATE_RECORD)
        
        await su_service.create_student(student, db)
        return SU.CREATED
