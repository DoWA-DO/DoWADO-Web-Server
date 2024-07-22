"""
진로 상담 챗봇 API - 컨트롤러
"""
import asyncio
from datetime import datetime
from typing import Annotated
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Security
import openai
from src.api.v1.login.login_control import get_current_user
from src.core.status import Status, SU, ER
from src.api.v1.chat import chatbot_service
from src.api.v1.chat.chatbot_dto import ChatRequest, ChatResponse
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/careerchat", tags=["진로 추천 챗봇 관련 API"])


# 유저 아이디(추후 로그인 정보 입력 받기)
@router.post(
    "/new-session",
    summary     = "새로운 채팅 시작하기 버튼",
    description = "- 새로운 채팅 세션 생성, 채팅을 위한 초기값들 초기화, ChatGenerator 객체 생성",
    responses   = Status.docs(SU.SUCCESS)
)
def create_chatbot_session():    
    session_id = chatbot_service.create_chatbot_session() 
    return {"session_id" : session_id}



@router.post(
    "/chat",
    summary        = "진로 상담 챗봇에게 채팅 메시지 전송하기 버튼",
    description    = "- 채팅 메시지를 기입 후 전송하면, 챗봇의 답장이 반환됨./ 이전 채팅 세션 이어서 채팅 가능",
    response_model = ChatResponse,
    responses      = Status.docs(SU.SUCCESS)
)
async def create_chatbot_message(
    session_id: str,
    input_query: str,
):
    try:
        response = await chatbot_service.get_chatbot_message(session_id, input_query)
        return response
    except Exception as e:
        logger.error(f"챗봇 세션 생성 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="챗봇 세션 생성 중 오류가 발생했습니다.")
    # response = await chatbot_service.get_chatbot_message(session_id, input_query)
    # return response



@router.post(
    "/save-chatlog",
    summary     = "채팅화면에서 뒤로가기 버튼 : 미완료된(진행중인) 진로상담 내용 임시 저장",
    description = "- Redis에 임시 저장된 채팅 내용을 RDB에 저장/ 이전 채팅 이력 수정 후 다시 저장 가능",
    responses   = Status.docs(SU.SUCCESS),
)
async def create_chatlog(
    session_id: str,
    current_user: dict = Security(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    username = current_user['username']
    await chatbot_service.create_chatlog(session_id, username, db)
    return SU.CREATED
