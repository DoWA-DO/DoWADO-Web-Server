"""
진로 상담 챗봇 API - DAO(ORM 쿼리문 작성)
"""
from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import joinedload, query

# from src.database.models import 
# from src.api.v1.chat.careerchat_dto import 
from src.database.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


