from src.api.v1.chat.chat_dto import ChatRequest, ChatResponse
from src.api.v1.chat import chat_dao

# 사용되지 않는 모듈은 삭제될 예정입니다.
from sqlalchemy.ext.asyncio import AsyncSession


# async def send_message(query) -> str:
#     await chat_dao.