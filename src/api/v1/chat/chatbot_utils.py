"""
진로 상담 챗봇 API - 채팅 메시지 생성
"""
import os
import openai
import redis
import uuid
import pickle
from typing import NewType
from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.core.config import settings
from src.api.v1.chat.chatbot_constants import contextualize_q_prompt, qa_prompt
import logging
from dotenv import load_dotenv

load_dotenv()  # .env 파일에 정의된 환경 변수를 로드합니다

# 로거 설정
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

# 환경 변수에서 API 키 로드
api_key = os.getenv("OPENAI_KEY")
if not api_key:
    raise ValueError("API 키가 설정되지 않았습니다. .env 파일이나 환경 변수에서 OPENAI_KEY를 설정해주세요.")
headers = {
    "Authorization": f"Bearer {api_key}"
}

openai.api_key = api_key
redis_client = redis.Redis.from_url(settings.Idx.REDIS_URL)

# ChatID = NewType('ChatID', str)

class ChatBase:
    def __init__(self):
        self._SIMILARITY_THRESHOLD = 0.15
        _logger.info("모델 초기화: %s, 온도: %s", settings.Idx.model_name, settings.Idx.temperature)
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
        _logger.info(f"벡터 스토어 초기화: {collection_name}")
        _embeddings = OpenAIEmbeddings(model = settings.Idx.embed_model)
        vector_store = PGVector(
            connection = "postgresql+psycopg://dowado:1234@localhost:6024/postgres", # 벡터 DB 주소
            embeddings = _embeddings,                         # 임베딩 함수
            # embedding_length = settings.Idx.embedding_length, # 임베딩 벡터 길이 제약,
            collection_name = collection_name,                # 벡터스토어 컬렉션 이름(=그룹명)
            distance_strategy = "cosine",                     # 유사도 측정 기준, l2, cosine, inner
            pre_delete_collection = False,                    # 테스트 시 True -> 기존 컬렉션 삭제
            use_jsonb = True,                                 # json보다 성능 좋음     
        )
        return vector_store


    # QI 케이스 구분완료
    def _init_retriever(self, vector_store, search_type: str, search_kwargs: Optional[Dict] = None):
        ''' Retriever 초기화 '''
        _logger.info(f"리트리버 초기화: 검색 유형 = {search_type}")
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
            raise ValueError(f"유효하지 않은 검색 유형: {search_type}")
    
    # job info
    def _init_jobinfo_chain(self):
        ''' chain 초기화
        create_stuff_documents_chain[현재 사용] : 문서 목록을 가져와서 모두 프롬프트로 포맷한 다음 해당 프롬프트를 LLM에 전달합니다.
        create_history_aware_retriever : 대화 기록을 가져온 다음 이를 사용하여 검색 쿼리를 생성하고 이를 기본 리트리버에 전달
        create_retrieval_chain : 사용자 문의를 받아 리트리버로 전달하여 관련 문서를 가져옵니다. 그런 다음 해당 문서(및 원본 입력)는 LLM으로 전달되어 응답을 생성
        '''
        _logger.info("잡 인포 체인 초기화")
        
        # 유저 질문 문맥화  
        history_aware_retriever = create_history_aware_retriever(
            self._llm, self.retriever_I, contextualize_q_prompt
        )       
        # 응답 생성 + 프롬프트 엔지니어링
        qa_chain = create_stuff_documents_chain(self._llm, qa_prompt)
        jobinfo_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

        _logger.info("잡 인포 체인 초기화 완료")
        return jobinfo_chain        



class ChatGenerator:
    def __init__(self, chat_base: ChatBase, session_id: str = None):
        self.chat_base = chat_base
        self.session_id = session_id or self.create_session_id()
        
    @classmethod
    def create_session_id(cls):
        ''' 새로운 채팅 세션 생성, 객체 생성 없이 호출 가능 '''
        session_id = str(uuid.uuid4())
        _logger.info(f"새로운 세션 ID 생성: {session_id}")
        return session_id
    
    def get_session_id(self):
        ''' 현재 객체의 session_id 반환 '''
        return self.session_id

    def generate_query(self, input_query: str) -> str:
        ''' 챗봇에게 쿼리 전송 '''
        def get_session_history(session_id: str) -> RedisChatMessageHistory:
            return RedisChatMessageHistory(session_id=session_id, url=settings.Idx.REDIS_URL)

        _logger.info(f"세션 ID {self.session_id}에 대한 쿼리 생성: 입력 = {input_query}")
        
        conversational_rag_chain = RunnableWithMessageHistory(
            self.chat_base.chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

        response = conversational_rag_chain.invoke(
            {"input": input_query},
            config={"configurable": {"session_id": self.session_id}}
        )

        # redis에 채팅기록 저장
        self.create_message_to_redis({"query": input_query, "response": response["answer"]})
        
        _logger.info(f'[응답 생성] 실제 모델 응답: response => \n{response}\n')
        _logger.info(f"[응답 생성] 세션 ID [{self.session_id}]에서 답변을 생성했습니다.")
        return response["answer"]


    def create_message_to_redis(self, message):
        ''' Redis에 메시지 저장 '''
        _logger.info(f"세션 ID {self.session_id}에 대한 메시지를 Redis에 저장")
        chat_history_key = f"chat_history:{self.session_id}"
        redis_client.rpush(chat_history_key, pickle.dumps(message))
    
    
    def get_chatlog_from_redis(self) -> list:
        ''' Redis에서 현재 객체의 session_id에 해당하는 채팅 로그 가져오기 '''
        _logger.info(f"세션 ID {self.session_id}에 대한 채팅 로그를 Redis에서 가져오기")
        chat_history_key = f"chat_history:{self.session_id}"
        chat_log = redis_client.lrange(chat_history_key, 0, -1) # redis에서 모든 요소 가져옴
        _logger.info(f'Redis에서 불러온 채팅기록: {chat_log}')
        if not chat_log:
            _logger.warning(f'채팅 기록이 비어 있습니다: {self.session_id}')
        return [pickle.loads(log) for log in chat_log]          # 역직렬화된 채팅 로그 항목들의 리스트를 반환


chatbot_instances: Dict[str, ChatGenerator] = {}

def init_chatbot_instance():
    ''' ChatBase에 기반한 챗봇 객체 생성 '''
    _logger.info("새로운 챗봇 인스턴스 초기화")
    chat_base = ChatBase()
    new_chatbot_instance = ChatGenerator(chat_base)
    session_id = new_chatbot_instance.session_id
    chatbot_instances[session_id] = new_chatbot_instance
    _logger.info(f'ChatBot 객체 생성: {new_chatbot_instance} for session_id: {session_id}')
    return session_id
