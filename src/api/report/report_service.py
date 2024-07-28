'''
수정 필요(레포트 API으로 이동 필)
'''
from fastapi import Request
from src.utils.use_model import Model
from src.utils.data_processing import preprocess_text_kiwi, label_decoding
from src.api.chat import chat_dao
from src.api.chat.chat_utils import chatbot_instances
from src.api.report import report_dao

import requests
import json
import logging


_logger = logging.getLogger(__name__)
model = Model()


async def save_chatlog_and_get_recommendation(session_id: str, student_email: str):
    ''' 채팅 로그를 저장하고 모델 추론을 수행 '''
    if session_id in chatbot_instances:
        
        ####################################### 채팅 로그 저장 #################################################
        chat_generator = chatbot_instances[session_id]
        chat_content = chat_generator.get_chatlog_from_redis()
        _logger.info(f'=>> 세션 ID : {session_id}, 채팅이력 : {chat_content}')
        
        # 채팅 로그 저장
        await report_dao.create_chatlog(session_id, chat_content, student_email)
        
        
        ######################################### 진로 추론 ####################################################
        # 채팅 로그에서 query와 response를 합친 텍스트 생성
        combined_text = " ".join([entry["query"] + " " + entry["response"] for entry in chat_content])
        _logger.info(f'로그 텍스트 병합 : {combined_text}')
        
        text = preprocess_text_kiwi(combined_text)
        pred = model.classify_dataframe(text)
        pred_decoded = label_decoding(pred)
        
        # 모델 추론 요청 (도커 컨테이너 버전)
        # response = requests.post(f"{DOCKER_URL}/predict", json={"text": combined_text})
        # if response.status_code != 200:
        #     raise ValueError("모델 추론 중 오류 발생")

        
        ########################################## 레포트 생성 ###################################################
        """
        [ 레포트 내용 ]
        - 예측한 진로(분야)
        - 해당 분야 직업 종류
        - 직업 상세 정보
        - 관련 학과 정보
        """
        
        # 레포트 생성
        
        return {'prediction': pred_decoded}
        # report = 
        # return {"prediction": pred_decoded, "report": report}
    else:
        _logger.error(f'입력 받은 session_id 에 chatbot_instance가 없습니다. session_id: {session_id}')
        raise ValueError("챗봇 인스턴스가 없습니다.")




async def get_chatlogs_by_teacher(teacher_email: str):
    ''' 선생님이 담당하는 학생들의 채팅 로그를 조회 '''
    chat_logs = await report_dao.get_chatlogs_by_teacher(teacher_email)
    return chat_logs


async def get_chatlogs_by_student(student_email: str):
    ''' 학생의 채팅 로그를 조회 '''
    chat_logs = await report_dao.get_chatlogs_by_student(student_email)
    return chat_logs
