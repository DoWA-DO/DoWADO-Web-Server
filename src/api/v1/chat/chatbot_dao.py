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
            chat_text=chat_request.message,
            chat_user=user_name,
            created_at=datetime.now().replace(microsecond=0)
        )
        self.db.add(chat)
        await self.db.commit()
        await self.db.refresh(chat)
        return ChatCreateResponse(
            id=chat.id,
            message=chat.chat_content,
            user_name=chat.chat_student_email,
            created_at=chat.chat_date,
            status=chat.chat_status 
        )
        
    #Read    
    async def get_chat_history(self) -> List[ChatLog]:
        chats = await self.db.execute(
            select(ChatLog)
            #.where(Chat.chat_user == chat_user)
            .order_by(ChatLog.chat_date.desc())
        )
        return chats.scalars().all()
    
    #Delete
    async def delete_chats_by_user(self, chat_student_email: str) -> None:
        await self.db.execute(delete(ChatLog).where(ChatLog.chat_student_email == chat_student_email)) # delete
        await self.db.commit()