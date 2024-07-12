# chatbot_dto.py

import json
from pydantic import BaseModel
from datetime import datetime

class ChatCreateRequest(BaseModel):
    chat_content: str

class ChatCreateResponse(BaseModel):
    id: int
    chat_content: str
    chat_student_email: str
    chat_date: datetime
    chat_status: int
