"""
회원(학생) 권한 API
- 학생 회원가입
- 마이페이지(개인정보 조회)
- 학생 비밀번호 수정
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Security
from src.config.status import Status, SU, ER
from src.api.user_students.student_dto import ReadStudentInfo, CreateStudent, UpdateStudent
from src.api.user_students import student_service
from src.config.security import JWT
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/student", tags=["회원(학생) 계정 관련 API"])

@router.post(
    "/sign-up",
    summary="회원가입",
    description="- String-Form / Boolean-Form / String-Form / String-Form / String-Form",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def create_student(student: Optional[CreateStudent]):
    logger.info("----------신규 학생 생성----------")
    await student_service.create_student(student)
    return SU.CREATED

@router.get(
    "/read",
    summary="개인 정보 조회",
    description="- 개인 정보 조회",
    response_model=ReadStudentInfo,
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
async def get_student(current_user: dict = Security(JWT.get_current_user)) -> ReadStudentInfo:
    logger.info("----------개인 정보 조회----------")
    try:
        username = current_user['username']
        if username is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        student_info = await student_service.get_student(username)
        logger.info(student_info)
        return ReadStudentInfo(
            student_email=student_info.student_email,
            student_name=student_info.student_name,
            student_school=student_info.student_school,
            student_grade=student_info.student_grade,
            student_class=student_info.student_class,
            student_number=student_info.student_number
        )
    except Exception as e:
        logger.error(f"Error getting student info: {e}")
        raise HTTPException(status_code=404, detail="Student not found")

@router.put(
    "/update",
    summary="학생 비밀번호 수정",
    description="- 현재 로그인된 학생의 비밀번호 수정",
    responses=Status.docs(SU.CREATED, ER.UNAUTHORIZED)
)
async def update_student(
    student_info: Optional[UpdateStudent],
    current_user: dict = Security(JWT.get_current_user)
):
    username = current_user['username']
    logger.info("----------기존 학생 비밀번호 수정----------")
    await student_service.update_student(username, student_info)
    return SU.SUCCESS
