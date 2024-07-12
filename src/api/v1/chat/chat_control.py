"""
진로 상담 챗봇 API
"""
from typing import Annotated
from typing import Optional
from fastapi import APIRouter, Depends
from src.core.status import Status, SU, ER
import logging

# (db 세션 관련)이후 삭제 예정, 개발을 위해 일단 임시로 추가
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db

# 호출할 모듈 추가
from src.api.v1.chat import chat_service
from src.api.v1.chat.chat_dto import ChatRequest, ChatResponse

# 로깅 및 라우터 객체 생성 - 기본적으로 추가
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/example", tags=["Career-Counseling-Chatbot"])



@router.post(
    "/",
    summary        = "진로 상담 챗봇에게 채팅 메세지 전송",
    description    = "- 진로 상담 챗봇에게 유저(학생)가 입력한 채팅 메세지를 전송, 챗봇의 답장이 반환됨",
    response_model = ChatResponse,
    responses      = Status.docs(SU.SUCCESS, ER.INVALID_TOKEN)
)
async def send_message(
    query: ChatRequest,
):
    response = await chat_service.send_message(query.query)
    return ChatResponse(response=response)

