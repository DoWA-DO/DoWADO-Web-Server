# chatbot_dto.py

from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from pydantic import ValidationError, validate_call

class ChatCreateRequest(BaseModel):
    chat_content: str
    chat_status: int

class ChatCreateResponse(BaseModel):
    id: int
    chat_content: str
    chat_student_email: str
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
    
    
