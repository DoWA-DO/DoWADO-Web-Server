"""
진로 상담 챗봇 API - 채팅 메시지 생성
"""
import openai
import redis
import uuid
from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.config import settings
from src.database.session import DATABASE_URL
import logging


_logger = logging.getLogger(__name__)
openai.api_key = settings.general.OPENAI_API_KEY


def generate_session_id() -> str:
    ''' UUID로 새로운 세션 ID 발급 '''
    return str(uuid.uuid4()) # 네트워크 상에서 중복되지 않는 고유 ID (범용 고유 식별자)


class ChatBase:
    def __init__(self):
        self.SIMILARITY_THRESHOLD = 0.15
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.vector_store_careerquestion = self._init_vector_store()
        self.vector_store_jobinfo = self.
        self.retriever = self.init_retriever()
        self.chain = self.init_chain()

    def _init_vector_store(self, collection_name: str):
        _embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        _vector_store = PGVector(
            connection = DATABASE_URL,         # 벡터 DB 주소
            embeddings = _embeddings,          # 임베딩 함수
            embedding_length = 512,            # 768, 임베딩 벡터 길이 제약,
            collection_name = collection_name, # 벡터스토어 컬렉션 이름(=그룹명)
            distance_strategy = "COSINE",      # 유사도 측정 기준
            pre_delete_collection = False,     # 테스트 시 True -> 기존 컬렉션 삭제
            use_jsonb = True,                  # json보다 성능 좋음     
        )
        _logger.info('=>> [Idx] 벡터 DB 초기값 설정')
        return _vector_store






class ChatGenerator:
    def __init__(self) -> None:
        ...
    

