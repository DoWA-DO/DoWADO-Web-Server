"""
진로 상담 챗봇 API - 서비스(비즈니스로직 처리)
"""
from fastapi import Request
from src.api.chat import chat_dao, chat_utils
from src.api.chat.chat_dto import ChatRequest, ChatResponse
from src.api.chat.chat_utils import chat_generation


async def create_chatbot_session(request: Request):
    ''' 새로운 채팅 세션 생성 '''
    session_id = chat_utils.generate_session_id()
    return {"session_id": session_id}
        

async def get_chatbot_message(input_query: str):
    response = chat_generation(input_query=input_query)
    return response