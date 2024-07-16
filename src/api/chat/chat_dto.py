"""
진로 상담 챗봇 API - DTO(데이터 전송 객체 선언)
"""
from datetime import datetime, timezone
from typing import Optional, Annotated
from fastapi import Depends, Form, Path
from pydantic import Field, EmailStr, validator
from src.config.dto import BaseDTO


class ChatRequest(BaseDTO):
    query: str
    session_id: str


class ChatResponse(BaseDTO):
    response: str
    session_id: str