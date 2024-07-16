"""
생명주기 이벤트 확장 모듈
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database.session import rdb
import logging

_logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션 주요 생명주기 이벤트를 관리하는 함수
    - FastAPI 애플리케이션 인스턴스에 대한 이벤트 핸들러 등록
    - 특정 이벤트 발생 시(예, ML 호출 등) 해당 함수 호출
    """
    # 시작 이벤트 처리
    _logger.info('애플리케이션 시작 중: 데이터베이스 테이블 생성')
    await rdb.create_tables()
        
    yield  # 요청 처리를 시작

    # 종료 이벤트 처리
    _logger.info('애플리케이션 종료 중: 데이터베이스 연결 해제')
    await rdb.dispose_engine()
    
def use(app: FastAPI):
    """ 이벤트 확장 모듈 사용 """
    app.lifespan_context = lifespan
    