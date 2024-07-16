"""
진로 상담 챗봇 API - 채팅 메시지 생성
"""
import redis
from typing import Dict, List, Optional
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI



def generation():
    ...
    
    
class ChatGenerator:
    def __init__(self):
        self.SIMILARITY_THRESHOLD = 0.15
        self.llm = ChatOpenAI(
            model = "gpt-3.5-turbo",
            temperature= 0
        )
        
        
    def init_vector_store(self):
        ''' Vector Store 초기화 '''
        embeddings = ""