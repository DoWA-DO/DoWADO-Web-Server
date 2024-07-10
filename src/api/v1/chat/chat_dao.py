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
from src.database.model import Chat, Teacher
from src.database.session import get_db
from src.api.v1.login.login_control import get_current_user
import logging

# Read
async def get_chat(db: AsyncSession, current_user: Teacher = Depends(get_current_user)) -> list[ReadChatInfo]:  # = Depends(get_db)
    result = await db.execute(select(Chat).filter(Chat.chat_user == current_user))
    chat_info = result.scalars().all()
    return [ReadChatInfo.from_orm(chat) for chat in chat_info]


# Create
async def create_chat(chat: CreateChat, db: AsyncSession, current_user: Teacher = Depends(get_current_user)) -> None:
    logging.info(f"current_user info: {current_user}")
    chat_data = chat.dict()
    chat_data["chat_user"] = current_user
    
    new_chat = Chat(**chat_data)
    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)
    
"""
# Update
async def update_chat(chat_name: str, chat_info: UpdateChat, db: AsyncSession) -> None:
    await db.execute(update(Chat).filter(Chat.chat_name==chat_name).values(chat_info.dict()))
    await db.commit()
"""    

# Delete
# 최근 대화 내역 1개 삭제 or 리셋 (나중에 구현)
async def delete_chat(db: AsyncSession, current_user: Teacher = Depends(get_current_user)) -> None:
    await db.execute(delete(Chat).where(Chat.chat_user == current_user))
    await db.commit()
    