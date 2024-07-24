"""
레포트 생성 관련 RAG 설정 및 유틸리티
"""
import logging
from typing import Optional
from langchain_openai import ChatOpenAI
from src.config import settings


logger = logging.getLogger(__name__)

