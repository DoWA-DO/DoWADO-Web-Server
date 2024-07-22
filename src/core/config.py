"""
전역 상수 초기화
"""

import logging
import logging.config
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class RDBSettings(BaseSettings):
    DB_PROTOCAL: str = "postgresql+asyncpg"  # 환경변수에 저장해야 함
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "0222"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "test"

    #DATABASE_URL = f"{DB_PROTOCAL}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DB_PROTOCAL}://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

# secret key 생성 : openssl rand -hex 32
SECRET_KEY = "8a4bab952b4e4317af926571fb93f1820f6929ba9c7c70b7969b1a01ec92757f"

# 네이버 메일 서버
NAVER_EMAIL = "example@naver.com" 
NAVER_PASSWORD = "example"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        },
        "detailed": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "detailed",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
    "loggers": {
        "uvicorn": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
    
    
    
class IdxSettings(BaseSettings):
    model_name: str = "gpt-3.5-turbo-1106" # gpt-3.5-turbo gpt-4-turbo
    temperature: int = 0
    context_window: int = 4096 # 16385(3.5) 128000(4)
    output_token: int = 1024 # 4096
    chunk_overlap: int = 0
    chunk_size: int = 512
    embed_model: str = "text-embedding-ada-002" # "intfloat/e5-small"
    
    # 추가 옵션
    embedding_length: int = 512 # 768, 임베딩 벡터 길이 제약
    
    # search type : similarity(코사인유사도), mmr(mmr알고리즘, 다양성에 집중), similarity_score_threshold(유사도 기준값 지정 버전)
    retriever_Q_search_type: str = "mmr"
    retriever_I_search_type: str = "similarity"
    
    # Chat DB
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"
    

class Settings(BaseSettings):
    #general: GeneralSettings = GeneralSettings()
    rdb: RDBSettings = RDBSettings()
    #jwt: JWTSettings = JWTSettings()
    # mail: SMTPSettings = SMTPSettings()
    Idx: IdxSettings = IdxSettings()
    
settings = Settings()