"""
데이터베이스 세션 연결 및 설정
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession # 비동기
from src.core.config import settings

# pip install asyncpg
# url = postgresql+asyncpg://{user}:{pwd}@server/db name
DATABASE_URL = settings.DATABASE_URL

# 비동기 엔진 생성
AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,    # SQL 문장 로그로 출력
    future=True,  # SQLAlchemy 2.0 스타일 활성화
    )

# 비동기 세션 생성
AsyncSessionLocal = sessionmaker(
    autocommit=False,  # 자동 커밋
    autoflush=False,   # 세션 변동사항 데이터베이스 자동 반영
    bind=AsyncEngine,      # 세션을 통해 실행되는 SQL 명령에 사용될 엔진 지정
    class_=AsyncSession,
    expire_on_commit=False
    )
        
# 데이터베이스 세션 생성
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session