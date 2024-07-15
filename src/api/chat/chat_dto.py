"""
진로 상담 챗봇 API - DTO(데이터 전송 객체 선언)
"""
from datetime import datetime, timezone
from typing import Optional, Annotated
from fastapi import Depends, Form, Path
from pydantic import Field, EmailStr, validator
from src.settings.dto import BaseDTO


# class CreateChatSession(BaseDTO):
#     chat_session_id: str = Field(..., description="채팅 세션 아이디")
#     chat_content: dict = Field(..., description="채팅 내용")
    
    
class ChatRequest(BaseDTO):
    query: str

    # stop_generating: bool = False

class ChatResponse(BaseDTO):
    response: str

    # sender: str
    # message: str
    # type: str
    # user_query: str = ""
    # user_id: str = ""