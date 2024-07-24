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

# 임시
DOCKER_URL = "http://localhost:8000"

def create_chatbot_session():
    ''' 새로운 ChatBase 객체 생성 -> 새로운 채팅 세션 생성 '''
    session_id = init_chatbot_instance()
    return session_id
    


async def get_chatbot_message(session_id: str, input_query: str):
    ''' 챗봇에게 채팅 쿼리 보내기 '''
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
    



'''
수정 필요(임시)
'''
from src.api.chat.report_model import Model
from src.api.chat.report_data_processing import preprocess_text_kiwi, label_decoding


model = Model()

async def save_chatlog_and_get_recommendation(session_id: str, student_email: str):
    ''' 채팅 로그를 저장하고 모델 추론을 수행 '''
    if session_id in chatbot_instances:
        chat_generator = chatbot_instances[session_id]
        chat_content = chat_generator.get_chatlog_from_redis()
        _logger.info(f'=>> 세션 ID : {session_id}, 채팅이력 : {chat_content}')
        
        # 채팅 로그 저장
        await chat_dao.create_chatlog(session_id, chat_content, student_email)
        
        # 채팅 로그에서 query와 response를 합친 텍스트 생성
        combined_text = " ".join([entry["query"] + " " + entry["response"] for entry in chat_content])
        _logger.info(f'로그 텍스트 병합 : {combined_text}')
        
        
        ############### 임시 병합 #################
        text = preprocess_text_kiwi(combined_text)
        pred = model.classify_dataframe(text)
        pred_decoded = label_decoding(pred)
        temp = {'prediction': pred_decoded}
        return temp
        
        
        # 모델 추론 요청 (컨테이너 버전)
        # response = requests.post(f"{DOCKER_URL}/predict", json={"text": combined_text})
        # if response.status_code != 200:
        #     raise ValueError("모델 추론 중 오류 발생")
        
        # return response.json()
    else:
        _logger.error(f'입력 받은 session_id 에 chatbot_instance가 없습니다. session_id: {session_id}')
        raise ValueError("챗봇 인스턴스가 없습니다.")
