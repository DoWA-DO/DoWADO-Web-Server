"""
API 개발 시 참고 : 프론트엔드에서 http 엔드포인트를 통해 호출되는 메서드
"""
# 기본적으로 추가
from typing import Annotated
from typing import Optional
from fastapi import APIRouter, Depends
from src.core.status import Status, SU, ER
import logging

# (db 세션 관련)이후 삭제 예정, 개발을 위해 일단 임시로 추가
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db

# 호출할 모듈 추가
from src.api.v1.teacher.teacher_dto import ReadTeacherInfo, CreateTeacher, UpdateTeacher, keyTeacher
from src.api.v1.teacher import teacher_service


# 로깅 및 라우터 객체 생성 - 기본적으로 추가
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/teacher", tags=["teacher"])

# 라우터 추가 시 현재는 src.api.v1.__init__.py에 생성하려는 라우터 추가해줘야 함.(수정 예정)


# Read
@router.get(
    "/",
    summary="전체 교원 조회",
    description="- 전체 교원 리스트 반환, 등록된 교원이 없는 경우 `[]` 반환",
    response_model=list[ReadTeacherInfo],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
# 함수명 get, post, update, delete 중 1택 + 목적에 맞게 이름 작성
async def get_teacher(db: AsyncSession = Depends(get_db)):
    # 개발 중 logging 사용하고 싶을 때 이 코드 추가
    logger.info("----------전체 교원 목록 조회----------")
    teacher_info = await teacher_service.get_teacher(db)
    return teacher_info


# Create
@router.post(
    "/",
    summary="입력 받은 교원 데이터를 데이터베이스에 추가",
    description="- String-Form / Boolean-Form / String-Form / String-Form / String-Form",
    # response_model=ResultType, # -> 코드 미완성, 주석처리
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def create_teacher(
    teacher: Optional[CreateTeacher],
    db: AsyncSession = Depends(get_db)
):
    logger.info("----------신규 교원 생성----------")
    await teacher_service.create_teacher(teacher, db)
    return SU.CREATED


# Update
@router.put(
    "/",
    summary="입력 받은 데이터로 변경 사항 수정",
    description="- email이 일치하는 데이터의 비밀번호, 이름, 학교이름 수정",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def update_teacher(
    teacher_email: str,  # JWT 토큰에서 id 가져오는 방식으로 변경, 이건 임시조치
    teacher_info: Optional[UpdateTeacher],
    db: AsyncSession = Depends(get_db)
):
    logger.info("----------기존 교원 수정----------")
    await teacher_service.update_teacher(teacher_email, teacher_info, db)
    return SU.SUCCESS


# Delete, 교원 삭제는 super_teacher 쪽으로 이동 해야 함. - TODO
@router.delete(
    "/",
    summary="교원 삭제",
    description="- 교원 이메일이 일치하는 데이터 삭제",
    responses=Status.docs(SU.SUCCESS, ER.DUPLICATE_RECORD),
)
async def delete_teacher(
    teacher_email: str, # JWT 토큰에서 id 가져오는 방식으로 변경, 임시조치
    db: AsyncSession = Depends(get_db)
):
    await teacher_service.delete_teacher(teacher_email, db)
    return SU.SUCCESS