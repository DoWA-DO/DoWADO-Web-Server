#chatbot_dao.py

from sqlalchemy import delete, func, text
from sqlalchemy.sql.expression import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1.chat.chatbot_dto import ChatCreateRequest, ChatCreateResponse
from src.database.model import ChatLog
from datetime import datetime

class ChatDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    #Create
    async def create_chat(self, user_name: str, chat_request: ChatCreateRequest) -> ChatCreateResponse:
        chat = ChatLog(
            chat_content=chat_request.chat_content,
            chat_student_email=user_name,
            chat_date=datetime.now().replace(microsecond=0),
            chat_status=0
        )
        self.db.add(chat)
        await self.db.commit()
        await self.db.refresh(chat)
        return ChatCreateResponse(
            id=chat.id,
            chat_content=chat.chat_content,
            chat_student_email=chat.chat_student_email,
            chat_date=chat.chat_date,
            chat_status=chat.chat_status 
        )
        
    #Read    
    async def get_chat_history(self, chat_user: str) -> List[ChatLog]:
        chats = await self.db.execute(
            select(ChatLog)
            .where(ChatLog.chat_student_email == chat_user)
            .order_by(ChatLog.chat_date.desc())
        )
        return chats.scalars().all()
    
    #Delete
    async def delete_chats_by_user(self, chat_student_email: str) -> None:
        await self.db.execute(delete(ChatLog).where(ChatLog.chat_student_email == chat_student_email)) # delete
        await self.db.commit()