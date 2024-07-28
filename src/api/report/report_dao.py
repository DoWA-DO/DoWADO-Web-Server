"""
진로 추천 레포트 API
"""
import json
import logging
from fastapi import Depends
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import Session, joinedload, query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import ChatLog, UserStudent
from src.database.session import AsyncSession, rdb


_logger = logging.getLogger(__name__)

@rdb.dao(transactional=True)
async def create_chatlog(session_id: str, chat_content: list, student_email: str, session: AsyncSession = rdb.inject_async()) -> None:
    ''' ChatLOG 테이블에 완료된(레포트를 생성완료한) 채팅 내역 저장하기 '''
    
    # 먼저 해당 세션 ID가 존재하는지 확인
    existing_chatlog = await session.execute(select(ChatLog).where(ChatLog.chat_session_id == session_id))
    existing_chatlog = existing_chatlog.scalars().first()

    if existing_chatlog:
        # 세션 ID가 존재하면 업데이트
        await session.execute(update(ChatLog).where(ChatLog.chat_session_id == session_id).values(
            chat_content=json.dumps(chat_content),
            chat_date=datetime.now(timezone.utc),
            chat_status=True,
            student_email=student_email
        ))
        _logger.info(f'기존 채팅 로그 업데이트: {session_id}')
    else:
        # 세션 ID가 존재하지 않으면 새로 삽입
        chatlog = ChatLog(
            chat_session_id=session_id,
            chat_content=json.dumps(chat_content),
            chat_date=datetime.now(timezone.utc),
            chat_status=True,
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
        
@rdb.dao()
async def get_chatlogs_by_teacher(teacher_email: str, session: AsyncSession = rdb.inject_async()):
    ''' 선생님 이메일로 해당 선생님이 담당하는 학생들의 채팅 로그 조회 (chat_status가 True인 항목만) '''
    result = await session.execute(
        select(ChatLog)
        .join(UserStudent, ChatLog.student_email == UserStudent.student_email)
        .where(UserStudent.teacher_email == teacher_email)
        .where(ChatLog.chat_status == True)  # chat_status가 True인 항목만 필터링
    )
    return result.scalars().all()


@rdb.dao()
async def get_chatlogs_by_student(student_email: str, session: AsyncSession = rdb.inject_async()):
    ''' 학생 이메일로 해당 학생의 채팅 로그 조회 '''
    result = await session.execute(
        select(ChatLog)
        .where(ChatLog.student_email == student_email)
    )
    return result.scalars().all()
