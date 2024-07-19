#teacher_control.py

"""
API 개발 시 참고 : 프론트엔드에서 http 엔드포인트를 통해 호출되는 메서드
"""
# 기본적으로 추가
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Security
from src.api.v1.login.login_control import get_current_user
from src.core.status import Status, SU, ER
import logging

# (db 세션 관련)이후 삭제 예정, 개발을 위해 일단 임시로 추가
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.model import UserTeacher
from src.database.session import get_db

# 호출할 모듈 추가
from src.api.v1.users.teacher.teacher_dto import CreateTeacher, ReadTeacherInfo, UpdateTeacher
from src.api.v1.users.teacher.teacher_dao import get_existing_user
from src.api.v1.users.teacher import teacher_service

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
# secret key 생성 : openssl rand -hex 32
SECRET_KEY = "8a4bab952b4e4317af926571fb93f1820f6929ba9c7c70b7969b1a01ec92757f"
ALGORITHM = "HS256"

# 로깅 및 라우터 객체 생성 - 기본적으로 추가
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/teacher", tags=["교직원"])

# Read
@router.get(
    "/read",
    summary = "개인 정보 조회",
    description = "- 개인 정보 조회",
    response_model = ReadTeacherInfo,
    responses = Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)

async def get_teacher(
    current_user: dict = Security(get_current_user),
    db: AsyncSession = Depends(get_db)
)-> ReadTeacherInfo:
    logger.info("----------개인 정보 조회----------")
    try:
        username = current_user['username']
        if username is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        teacher_info = await teacher_service.get_teacher(username, db)
        logger.info(teacher_info)
        return ReadTeacherInfo(
            teacher_email=teacher_info.teacher_email,
            teacher_name=teacher_info.teacher_name,
            teacher_school=teacher_info.teacher_school,
            teacher_grade=teacher_info.teacher_grade,
            teacher_class=teacher_info.teacher_class,
        )
    except Exception as e:
        logger.error(f"Error getting teacher info: {e}")
        raise HTTPException(status_code=404, detail="Teacher not found")
    
# Create
@router.post(
    "/signup",
    summary = "회원가입",
    description = "- String-Form / Boolean-Form / String-Form / String-Form / String-Form",
    # response_model=ResultType, # -> 코드 미완성, 주석처리
    responses = Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def create_teacher(
    teacher: Optional[CreateTeacher],
    db: AsyncSession = Depends(get_db)
):
    logger.info("----------신규 교원 생성----------")
    
    # 중복 여부 확인
    existing_teacher = await get_existing_user(db, teacher)
    if existing_teacher:
        raise HTTPException(status_code=409, detail=ER.DUPLICATE_RECORD)
    
    await teacher_service.create_teacher(teacher, db)
    return SU.CREATED


# Update
@router.put(
    "/update",
    summary = "교원 비밀번호 수정",
    description = "- 현재 로그인된 선생님의 비밀번호 수정",
    responses=Status.docs(SU.CREATED, ER.UNAUTHORIZED)
)
async def update_teacher(
    teacher_info: Optional[UpdateTeacher],
    current_user: dict = Security(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    username = current_user['username']
    logger.info("----------기존 교원 비밀번호 수정----------")
    await teacher_service.update_teacher(teacher_info, username, db)
    return SU.SUCCESS

'''
# Delete
@router.delete(
    "/delete",
    summary="교원 데이터 삭제",
    description="- 교원 이메일이 일치하는 데이터 삭제",
    responses=Status.docs(SU.SUCCESS, ER.DUPLICATE_RECORD),
)
async def delete_teacher(
    teacher_email: str, # JWT 토큰에서 id 가져오는 방식으로 변경, 임시조치
    db: AsyncSession = Depends(get_db)
):
    await teacher_service.delete_teacher(teacher_email, db)
    return SU.SUCCESS
'''