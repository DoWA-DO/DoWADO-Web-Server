"""
진로 상담 챗봇 API - 채팅 메시지 생성
"""
import openai
import redis
import uuid
from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.config import settings


openai.api_key = settings.general.OPENAI_API_KEY


def generate_session_id() -> str:
    ''' UUID로 새로운 세션 ID 발급 '''
    return str(uuid.uuid4()) # 네트워크 상에서 중복되지 않는 고유 ID (범용 고유 식별자)




class ChatBase:
    def __init__(self):
        self.SIMILARITY_THRESHOLD = 0.15
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.vector_store = self.init_vector_store()
        self.retriever = self.init_retriever()
        self.chain = self.init_chain()

    # def _init_vector_store(self):
    #     embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    #     vector_store = PGVector.from_documents(
    #         embedding= embeddings,
    #         documents= 
    #     )






class ChatGenerator:
    def __init__(self) -> None:
        ...
    

