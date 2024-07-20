"""
진로 상담 챗봇 API - 컨트롤러
"""
from typing import Annotated
from typing import Optional
from fastapi import APIRouter, Depends, Request
from src.config.status import Status, SU, ER
from src.api.chat import chat_service
from src.api.chat.chat_dto import ChatRequest, ChatResponse
import logging


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/careerchat", tags=["Career-Counseling-Chatbot"])


# 유저 아이디(추후 로그인 정보 입력 받기)
@router.post(
    "/new-session",
    summary     = "새로운 채팅 시작하기 버튼",
    description = "- 새로운 채팅 세션 생성, 채팅을 위한 초기값들 초기화, ChatGenerator 객체 생성",
    responses   = Status.docs(SU.SUCCESS)
)
def create_chatbot_session():    
    session_id = chat_service.create_chatbot_session() 
    return {"session_id" : session_id}



@router.post(
    "/chat",
    summary        = "진로 상담 챗봇에게 채팅 메시지 전송하기 버튼",
    description    = "- 채팅 메시지를 기입 후 전송하면, 챗봇의 답장이 반환됨./ 이전 채팅 세션 이어서 채팅 가능",
    response_model = ChatResponse,
    responses      = Status.docs(SU.SUCCESS, ER.INVALID_TOKEN)
)
async def create_chatbot_message(
    session_id: str,
    input_query: str,
):
    response = await chat_service.get_chatbot_message(session_id, input_query)
    return response



@router.post(
    "/save-chatlog",
    summary     = "채팅화면에서 뒤로가기 버튼 : 미완료된(진행중인) 진로상담 내용 임시 저장",
    description = "- Redis에 임시 저장된 채팅 내용을 RDB에 저장/ 이전 채팅 이력 수정 후 다시 저장 가능",
    responses   = Status.docs(SU.SUCCESS, ER.INVALID_TOKEN),
)
async def create_chatlog(
    session_id: str,
):
    await chat_service.create_chatlog(session_id)
    return SU.CREATED
