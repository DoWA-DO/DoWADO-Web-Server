"""
회원(교사) 권한 API
- 선생 (개인정보 조회)
- 선생 회원가입
- 선생 비밀번호 수정
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Security
from src.config.status import Status, SU, ER
from src.api.user_teachers.teacher_dto import CreateTeacher, ReadTeacherInfo, UpdateTeacher
from src.api.user_teachers import teacher_service
from src.config.security import JWT
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/teacher", tags=["회원(교직원) 계정 관련 API"])

@router.post(
    "/signup",
    summary="회원가입",
    description="- String-Form / Boolean-Form / String-Form / String-Form / String-Form",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def create_teacher(teacher: Optional[CreateTeacher]):
    logger.info("----------신규 교원 생성----------")
    await teacher_service.create_teacher(teacher)
    return SU.CREATED

@router.get(
    "/read",
    summary="개인 정보 조회",
    description="- 개인 정보 조회",
    response_model=ReadTeacherInfo,
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
async def get_teacher(current_user: dict = Security(JWT.get_current_user)) -> ReadTeacherInfo:
    logger.info("----------개인 정보 조회----------")
    try:
        username = current_user['username']
        if username is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        teacher_info = await teacher_service.get_teacher(username)
        logger.info(teacher_info)
        return ReadTeacherInfo(
            teacher_email=teacher_info.teacher_email,
            teacher_name=teacher_info.teacher_name,
            teacher_school=teacher_info.teacher_school,
            teacher_grade=teacher_info.teacher_grade,
            teacher_class=teacher_info.teacher_class
        )
    except Exception as e:
        logger.error(f"Error getting teacher info: {e}")
        raise HTTPException(status_code=404, detail="Teacher not found")

@router.put(
    "/update",
    summary="교원 비밀번호 수정",
    description="- 현재 로그인된 선생님의 비밀번호 수정",
    responses=Status.docs(SU.CREATED, ER.UNAUTHORIZED)
)
async def update_teacher(
    teacher_info: Optional[UpdateTeacher],
    current_user: dict = Security(JWT.get_current_user)
):
    username = current_user['username']
    logger.info("----------기존 교원 비밀번호 수정----------")
    await teacher_service.update_teacher(username, teacher_info)
    return SU.SUCCESS
