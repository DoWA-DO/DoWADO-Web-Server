"""
진로 상담 챗봇 API - 서비스(비즈니스로직 처리)
"""
from fastapi import Request
from src.api.chat import chat_dao, chat_utils
from src.api.chat.chat_dto import ChatRequest, ChatResponse


async def create_chatbot_session(request: Request):
    ''' 새로운 채팅 세션 생성 '''
    session_id = chat_utils.generate_session_id()
    return {"session_id": session_id}
        

async def get_chatbot_message(session_id: str, query: str):

