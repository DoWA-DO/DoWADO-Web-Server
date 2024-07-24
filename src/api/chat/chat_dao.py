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
async def create_chatlog(session_id: str, chat_content: list, student_email: str, session: AsyncSession = rdb.inject_async()) -> None:
    ''' ChatLOG 테이블에 미완료된(레포트를 생성하지 않은) 채팅 내역 저장하기 '''
    
    # 먼저 해당 세션 ID가 존재하는지 확인
    existing_chatlog = await session.execute(select(ChatLog).where(ChatLog.chat_session_id == session_id))
    existing_chatlog = existing_chatlog.scalars().first()

    if existing_chatlog:
        # 세션 ID가 존재하면 업데이트
        await session.execute(update(ChatLog).where(ChatLog.chat_session_id == session_id).values(
            chat_content=json.dumps(chat_content),
            chat_date=datetime.now(timezone.utc),
            chat_status=False,
            student_email=student_email
        ))
        _logger.info(f'기존 채팅 로그 업데이트: {session_id}')
    else:
        # 세션 ID가 존재하지 않으면 새로 삽입
        chatlog = ChatLog(
            chat_session_id=session_id,
            chat_content=json.dumps(chat_content),
            chat_date=datetime.now(timezone.utc),
            chat_status=False,
            student_email=student_email
        )
        await session.execute(insert(ChatLog).values({
            "chat_session_id": chatlog.chat_session_id,
            "chat_content": chatlog.chat_content,
            "chat_date": chatlog.chat_date,
            "chat_status": chatlog.chat_status,
            "student_email": chatlog.student_email
        }))
        _logger.info(f'새로운 채팅 로그 삽입: {session_id}')
        

# 내가 작성한거 전부(학생)
# 담당 학생들이 작성 완료한거(선생)
@rdb.dao(transactional=True)
async def get_chatlogs(session: AsyncSession = rdb.inject_async()) -> list:
    ''' ChatLog 테이블 전체 항목 조회하기 '''
    
    result = await session.execute(select(ChatLog))
    chatlogs = result.scalars().all()
    return chatlogs