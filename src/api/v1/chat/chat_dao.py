# chat_dao.py
"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 기본적으로 추가
from fastapi import Depends
from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload, query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.chat.chat_dto import ReadChatInfo, CreateChat
from src.database.model import Chat
from src.database.session import get_db


# Read
async def get_chat(db: AsyncSession) -> list[ReadChatInfo]:  # = Depends(get_db)
    result = await db.execute(select(Chat))
    chat_info = result.scalars().all()
    return chat_info


# Create
async def create_chat(chat: CreateChat, db: AsyncSession) -> None:
    await db.execute(insert(Chat).values(chat.dict())) # db:Chat table:chat
    await db.commit() # 자동으로 commit되게 설정 변경 필요
    
"""
# Update
async def update_chat(chat_name: str, chat_info: UpdateChat, db: AsyncSession) -> None:
    await db.execute(update(Chat).filter(Chat.chat_name==chat_name).values(chat_info.dict()))
    await db.commit()
"""    

# Delete
async def delete_chat(chat_name: str, db: AsyncSession) -> None:
    await db.execute(delete(Chat).where(Chat.chat_name == chat_name))
    await db.commit()
    