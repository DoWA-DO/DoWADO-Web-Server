# chat_service.py

"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 호출할 모듈 추가
from src.api.v1.chat.chat_dto import ReadChatInfo, CreateChat
from src.api.v1.chat import chat_dao
from src.database.model import Teacher

# 이후 삭제 예정, 일단 기본 추가
from sqlalchemy.ext.asyncio import AsyncSession


# Read
async def get_chat(db: AsyncSession, current_user: Teacher) -> list[ReadChatInfo]:
    chat_info = await chat_dao.get_chat(current_user, db)
    return chat_info

# Create
async def create_chat(chat: CreateChat, current_user: Teacher, db: AsyncSession) -> None:
    await chat_dao.create_chat(chat, db, current_user)
    
"""    
# Update
async def update_chat(chat_name: str, chat_info: UpdateChat, db: AsyncSession) -> None:
    await chat_dao.update_chat(chat_name, chat_info, db)
"""    

# Delete
async def delete_chat(chat_text: str, db: AsyncSession) -> None:
    await chat_dao.delete_chat(chat_text, db)