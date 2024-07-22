
"""
진로 상담 챗봇 API - DTO(데이터 전송 객체 선언)
"""
from datetime import datetime, timezone
from typing import Optional, Annotated
from fastapi import Depends, Form, Path
from pydantic import BaseModel, Field, EmailStr, ValidationError, validate_call, validators
from src.database.dto import BaseDTO





# class CreateChatInfo(BaseDTO):
#     chat_session_id: Annotated[str, Form(description="채팅 아이디(세션 아이디)")]
#     chat_status: Annotated[bool, Depends(lambda: True)] = Field(True, description="채팅 편집 가능(리포트 생성 전)")
#     chat_date: Annotated[datetime, Depends(lambda: datetime.now(timezone.utc))] = Field(
#         default_factory=lambda: datetime.now(timezone.utc), description="생성 시간"
#     )
    


class ChatRequest(BaseDTO):
    session_id: str
    query: str
    


class ChatResponse(BaseDTO):
    session_id: str
    response: str
    

class ChatCreateResponse(BaseModel):
    id: int
    chat_student_email: str
    chat_content: str
    chat_response:str
    chat_date: datetime
    chat_status: int
    
    @validate_call
    def foo(a: int):
        return a
    
    try:
        foo()
    except ValidationError as exc:
        print(repr(exc.errors()[0]['type']))
        #> 'missing_argument'