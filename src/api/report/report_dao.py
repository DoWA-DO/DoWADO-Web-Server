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
from src.database.models import ChatLog
from src.database.session import AsyncSession, rdb


_logger = logging.getLogger(__name__)

