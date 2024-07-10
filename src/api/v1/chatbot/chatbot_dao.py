#chatbot_dao.py

from sqlalchemy import delete
from sqlalchemy.sql.expression import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1.chatbot.chatbot_dto import ChatCreateRequest, ChatCreateResponse
from src.database.model import Chat
from datetime import datetime

class ChatDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_chat(self, user_name: str, chat_request: ChatCreateRequest) -> ChatCreateResponse:
        chat = Chat(
            chat_text=chat_request.message,
            chat_user=user_name,
            created_at=datetime.now().replace(microsecond=0)
        )
        self.db.add(chat)
        await self.db.commit()
        await self.db.refresh(chat)
        return ChatCreateResponse(
            id=chat.id,
            message=chat.chat_text,
            user_name=chat.chat_user,
            created_at=chat.created_at
        )
        
    async def get_chat_history(self, chat_user: str) -> List[Chat]:
        chats = await self.db.execute(
            select(Chat)
            .where(Chat.chat_user == chat_user)
            .order_by(Chat.created_at.desc())
        )
        return chats.scalars().all()
    
    async def delete_chats_by_user(self, chat_user: str) -> None:
        await self.db.execute(delete(Chat).where(Chat.chat_user == chat_user))
        await self.db.commit()