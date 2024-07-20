"""
진로 상담 챗봇 API - 서비스(비즈니스로직 처리)
"""
from fastapi import Request
from src.api.chat import chat_dao, chat_utils
from src.api.chat.chat_dto import ChatRequest, ChatResponse
from src.api.chat.chat_utils import init_chatbot_instance, chatbot_instances, redis_client
import logging


_logger = logging.getLogger(__name__)

def create_chatbot_session():
    ''' 새로운 ChatBase 객체 생성 -> 새로운 채팅 세션 생성 '''
    session_id = init_chatbot_instance()
    return session_id
    


async def get_chatbot_message(session_id: str, input_query: str):
    if session_id in chatbot_instances:
        response = chatbot_instances[session_id].generate_query(input_query=input_query)
        return ChatResponse(session_id=session_id, response=response)    
    else:
        _logger.error(f'입력 받은 session_id 에 chatbot_instance가 없습니다. session_id: {session_id}')
        return ChatResponse(session_id=session_id, response="챗봇 인스턴스가 없습니다.")