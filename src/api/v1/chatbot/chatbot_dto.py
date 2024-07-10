from pydantic import BaseModel
from datetime import datetime

class ChatCreateRequest(BaseModel):
    message: str

class ChatCreateResponse(BaseModel):
    id: int
    message: str
    user_name: str
    created_at: datetime
