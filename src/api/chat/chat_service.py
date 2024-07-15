"""
진로 상담 챗봇 API - 서비스(비즈니스로직 처리)
"""
from fastapi import Request
from src.api.chat import chat_dao

# 임시
from src.api.chat.chat_dto import ChatRequest, ChatResponse
from sqlalchemy.ext.asyncio import AsyncSession


async def create_chatbot_session(request: Request):
    ...
        
    