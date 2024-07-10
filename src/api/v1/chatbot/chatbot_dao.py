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
            created_at=datetime.now()
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

