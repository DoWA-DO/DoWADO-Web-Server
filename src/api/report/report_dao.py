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


@rdb.dao()
async def get_chatlogs_by_teacher(teacher_email: str, session: AsyncSession = rdb.inject_async()):
    ''' 선생님 이메일로 해당 선생님이 담당하는 학생들의 채팅 로그 조회 '''
    result = await session.execute(
        select(ChatLog)
        .join(UserStudent, ChatLog.student_email == UserStudent.student_email)
        .where(UserStudent.teacher_email == teacher_email)
    )
    return result.scalars().all()
