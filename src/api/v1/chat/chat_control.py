#chat_control.py

"""
API 개발 시 참고 : 프론트엔드에서 http 엔드포인트를 통해 호출되는 메서드
"""
# 기본적으로 추가
from typing import Annotated
from typing import Optional
from fastapi import APIRouter, Depends
from src.core.status import Status, SU, ER
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db

# 호출할 모듈 추가
from src.api.v1.chat.chat_dto import ReadChatInfo, CreateChat
from src.api.v1.chat import chat_service
from src.database.model import Teacher
from src.api.v1.login.login_control import get_current_user

# 로깅 및 라우터 객체 생성 - 기본적으로 추가
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["채팅"])

# Read
@router.get(
    "/read",
    summary="전체 대화 이력 조회",
    description="- 전체 대화 리스트 반환, 등록된 대화가 없는 경우 `[]` 반환",
    response_model=list[ReadChatInfo],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)

async def get_chat(
    db: AsyncSession = Depends(get_db),
    current_user: Teacher = Depends(get_current_user)
    ):
    # 개발 중 logging 사용하고 싶을 때 이 코드 추가
    logger.info("----------전체 대화 이력 조회----------")
    chat_info = await chat_service.get_chat(db, current_user)
    return chat_info


# Create
@router.post(
    "/create",
    summary="입력 받은 데이터를 데이터베이스에 추가",
    description="- Text-Form / Text-Form / Text-Form / date-Form",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def create_chat(
    chat: Optional[CreateChat],
    db: AsyncSession = Depends(get_db),
    current_user: Teacher = Depends(get_current_user)
):
    logger.info("----------신규 대화 생성----------")
    await chat_service.create_chat(chat, db, current_user)
    return SU.CREATED

"""
# Update
@router.put(
    "/update",
    summary="입력 받은 데이터로 변경 사항 수정",
    description="- name이 일치하는 데이터의 text, job, date 수정",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def update_chat(
    chat_name: str,  # JWT 토큰에서 id 가져오는 방식으로 변경, 이건 임시조치
    chat_info: Optional[UpdateChat],
    current_user: Teacher = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    logger.info("----------기존 대화 이력 수정----------")
    await chat_service.update_chat(chat_name, chat_info, db, current_user)
    return SU.SUCCESS
"""

# Delete
@router.delete(
    "/delete",
    summary="대화 이력 삭제",
    description="- username이 일치하는 데이터 삭제",
    responses=Status.docs(SU.SUCCESS, ER.DUPLICATE_RECORD),
)
async def delete_chat(
    chat_name: str, 
    current_user: Teacher = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await chat_service.delete_chat(chat_name, db, current_user)
    return SU.SUCCESS