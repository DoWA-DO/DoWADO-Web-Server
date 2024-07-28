"""
진로 상담 챗봇 API - 서비스(비즈니스로직 처리)
"""
from fastapi import Request
from src.api.chat import chat_dao, chat_utils
from src.api.chat.chat_dto import ChatRequest, ChatResponse
from src.api.chat.chat_utils import init_chatbot_instance, chatbot_instances, redis_client
import logging
import requests
import json


_logger = logging.getLogger(__name__)


def create_chatbot_session():
    ''' 새로운 ChatBase 객체 생성 -> 새로운 채팅 세션 생성 '''
    session_id = init_chatbot_instance()
    return session_id
    

async def get_chatbot_message(session_id: str, input_query: str):
    ''' 챗봇에게 채팅 쿼리 보내기 '''
    # 채팅 이어서하기 버튼이 있다면 새로운 api 만들고 거기로 옮기기
    if await chat_dao.get_chatlog_status(session_id):
        _logger.warning(f'session_id: {session_id}의 채팅 상태가 True입니다.(레포트 생성완료)')
        return ChatResponse(session_id=session_id, response="현재 세션에서 새로운 채팅을 시작할 수 없습니다.")
    else:
        if session_id in chatbot_instances:
            response = chatbot_instances[session_id].generate_query(input_query=input_query)
            return ChatResponse(session_id=session_id, response=response)    
        else:
            _logger.error(f'입력 받은 session_id 에 chatbot_instance가 없습니다. session_id: {session_id}')
            return ChatResponse(session_id=session_id, response="챗봇 인스턴스가 없습니다.")
    
        
async def create_chatlog(session_id: str, student_email: str):
    ''' 진로상담 기록 DB에 저장하기 '''
    if session_id in chatbot_instances:
        chat_generator = chatbot_instances[session_id]
        chat_content = chat_generator.get_chatlog_from_redis()
        _logger.info(f'=>> 세션 ID : {session_id}, 채팅이력 : {chat_content}')
        await chat_dao.create_chatlog(session_id, chat_content, student_email)
    else:
        _logger.error(f'입력 받은 session_id 에 chatbot_instance가 없습니다. session_id: {session_id}')
        raise ValueError("챗봇 인스턴스가 없습니다.")
    



