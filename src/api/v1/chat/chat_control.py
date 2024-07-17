# chat_control.py

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1.chat.chatbot_dto import ChatCreateResponse
from src.api.v1.login.login_control import get_current_user
from src.core.status import Status, SU, ER
from src.database.session import get_db

from .chatbot_control import router

@router.post(
    "/chat",
    summary="진로 상담 챗봇에게 채팅 메시지 전송",
    description="- 채팅 메시지를 기입 후 전송하면, 챗봇의 답장이 반환됨.",
    response_model = ChatCreateResponse,
    responses = Status.docs(SU.SUCCESS, ER.INVALID_TOKEN)
)
async def create_chatbot_message(
    query: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    username = current_user.get('username')
    response = await create_chatbot_message(query, username, db)
    return response