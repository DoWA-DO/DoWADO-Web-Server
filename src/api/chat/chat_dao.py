"""
진로 상담 챗봇 API - DAO(ORM 쿼리문 작성)
"""
from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import joinedload, query

from src.database.models import ChatLog
# from src.api.v1.chat.careerchat_dto import 
from src.database.session import AsyncSession, rdb
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
import json
import logging


_logger = logging.getLogger(__name__)

@rdb.dao(transactional=True)
async def create_chatlog(session_id: str, chat_content: list, session: AsyncSession = rdb.inject_async()) -> None:
    # 먼저 해당 세션 ID가 존재하는지 확인
    existing_chatlog = await session.execute(select(ChatLog).where(ChatLog.chat_session_id == session_id))
    existing_chatlog = existing_chatlog.scalars().first()

    if existing_chatlog:
        # 세션 ID가 존재하면 업데이트
        await session.execute(update(ChatLog).where(ChatLog.chat_session_id == session_id).values(
            chat_content=json.dumps(chat_content),
            chat_date=datetime.now(timezone.utc),
            chat_status=False
        ))
        _logger.info(f'기존 채팅 로그 업데이트: {session_id}')
    else:
        # 세션 ID가 존재하지 않으면 새로 삽입
        chatlog = ChatLog(
            chat_session_id=session_id,
            chat_content=json.dumps(chat_content),
            chat_date=datetime.now(timezone.utc),
            chat_status=False
        )
        await session.execute(insert(ChatLog).values({
            "chat_session_id": chatlog.chat_session_id,
            "chat_content": chatlog.chat_content,
            "chat_date": chatlog.chat_date,
            "chat_status": chatlog.chat_status
        }))
        _logger.info(f'새로운 채팅 로그 삽입: {session_id}')