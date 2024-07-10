from src.api.v1.chatbot.chatbot_dto import ChatCreateRequest, ChatCreateResponse
from src.api.v1.chatbot.chatbot_dao import ChatDAO
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.database.session import get_db

class ChatService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.chat_dao = ChatDAO(db)

    async def create_chat(self, user_name: str, chat_request: ChatCreateRequest) -> ChatCreateResponse:
        return await self.chat_dao.create_chat(user_name, chat_request)
