"""
진로 상담 챗봇 API - 채팅 메시지 생성
"""
import openai
import redis
import uuid
from typing import NewType
from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.config import settings
from src.database.session import DATABASE_URL
from src.api.chat.chat_constants import contextualize_q_prompt, qa_prompt
import logging


_logger = logging.getLogger(__name__)
openai.api_key = settings.general.OPENAI_API_KEY

ChatID = NewType('ChatID', str)

def generate_session_id() -> str:
    ''' UUID로 새로운 세션 ID 발급 '''
    return str(uuid.uuid4()) # 네트워크 상에서 중복되지 않는 고유 ID (범용 고유 식별자)




class ChatBase:
    def __init__(self):
        self._SIMILARITY_THRESHOLD = 0.15
        self._llm = ChatOpenAI(
            model       = settings.Idx.model_name, 
            temperature = settings.Idx.temperature,
        )
        self.vector_store_Q = self._init_vector_store("career_question_docs") # 벡터스토어 컬렉션 이름
        self.vector_store_I = self._init_vector_store("job_info_docs")
        self.retriever_Q = self._init_retriever(self.vector_store_Q, settings.Idx.retriever_Q_search_type)
        self.retriever_I = self._init_retriever(self.vector_store_I, settings.Idx.retriever_I_search_type)
        self.chain = self._init_jobinfo_chain()


    # QI 케이스 구분완료
    def _init_vector_store(self, collection_name: str):
        ''' Vector Store 초기화 '''
        _embeddings = OpenAIEmbeddings(model = settings.Idx.embed_model)
        vector_store = PGVector(
            connection = DATABASE_URL,                        # 벡터 DB 주소
            embeddings = _embeddings,                         # 임베딩 함수
            embedding_length = settings.Idx.embedding_length, # 임베딩 벡터 길이 제약,
            collection_name = collection_name,                # 벡터스토어 컬렉션 이름(=그룹명)
            distance_strategy = "COSINE",                     # 유사도 측정 기준
            pre_delete_collection = False,                    # 테스트 시 True -> 기존 컬렉션 삭제
            use_jsonb = True,                                 # json보다 성능 좋음     
        )
        return vector_store


    # QI 케이스 구분완료
    def _init_retriever(self, vector_store, search_type: str, search_kwargs: Optional[Dict] = None):
        ''' Retriever 초기화 '''
        
        if search_kwargs is None:
            search_kwargs = {}
        
        if search_type == "similarity":
            return vector_store.as_retriever(search_type=search_type, search_kwargs=search_kwargs)
        elif search_type == "mmr":
            search_kwargs.setdefault('lambda_mult', 0.5)
            search_kwargs.setdefault('fetch_k', 20)
            return vector_store.as_retriever(search_type=search_type, search_kwargs=search_kwargs)
        elif search_type == "similarity_score_threshold":
            search_kwargs.setdefault('score_threshold', self._SIMILARITY_THRESHOLD)
            return vector_store.as_retriever(search_type=search_type, search_kwargs=search_kwargs)
        else:
            raise ValueError(f"Invalid search type: {search_type}")
    
    # job info
    def _init_jobinfo_chain(self):
        ''' chain 초기화
        create_stuff_documents_chain[현재 사용] : 문서 목록을 가져와서 모두 프롬프트로 포맷한 다음 해당 프롬프트를 LLM에 전달합니다.
        create_history_aware_retriever : 대화 기록을 가져온 다음 이를 사용하여 검색 쿼리를 생성하고 이를 기본 리트리버에 전달
        create_retrieval_chain : 사용자 문의를 받아 리트리버로 전달하여 관련 문서를 가져옵니다. 그런 다음 해당 문서(및 원본 입력)는 LLM으로 전달되어 응답을 생성
        '''
        
        # 유저 질문 문맥화  
        history_aware_retriever = create_history_aware_retriever(
            self._llm, self.retriever_I, contextualize_q_prompt
        )       
        # 응답 생성 + 프롬프트 엔지니어링
        qa_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        jobinfo_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

        _logger.info("=>> jobinfo chain 초기화 완료")
        return jobinfo_chain        



class ChatGenerator:
    def __init__(self) -> None:
        ...
    

