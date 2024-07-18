"""
config : 프로젝트 전반에 공통으로 사용되는 모듈 모음
"""
"""
애플리케이션 환경 설정 및 로깅 설정 모듈
"""
from typing import Optional, Tuple, TypeVar, Type
from pathlib import Path
import json
import logging
import logging.config
import os
import sys
from dataclasses import dataclass
import dacite
from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings


# .env 파일에서 환경 변수 로드
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class GeneralSettings(BaseSettings):
    OPENAI_API_KEY: SecretStr
    DEBUG: bool = True
    API_DOC_VIEW: bool = True

class RDBSettings(BaseSettings):
    DB_PROTOCAL: str = "postgresql+psycopg"  # asyncpg | psycopg 이지만 psycopg3 사용(비동기가능/벡터DB+RDB) 
    DB_USERNAME: str = "dowado"
    DB_PASSWORD: str = SecretStr
    DB_HOST: str = "localhost"
    DB_PORT: str = "6024"
    DB_NAME: str = "postgres"

# class JWTSettings(BaseSettings):
#     JWT_SECRET_KEY: SecretStr
#     JWT_ACCESS_EXPIRE_MIN: int = 5
#     JWT_INV_ACCESS_EXPIRE_MIN: int = 1440
#     JWT_SESSION_EXPIRE_MIN: int = 30

# class SMTPSettings(BaseSettings):
#     MAIL_USERNAME: str = "rpamaster@rbrain.co.kr"
#     MAIL_PASSWORD: SecretStr
#     MAIL_FROM: str = "rpamaster@rbrain.co.kr"
#     MAIL_PORT: int = 587
#     MAIL_SERVER: str = "smtp-mail.outlook.com"
#     MAIL_STARTTLS: bool = True
#     MAIL_SSL_TLS: bool = False
#     USE_CREDENTIALS: bool = True
#     VALIDATE_CERTS: bool = True

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
    

class Settings(BaseSettings):
    general: GeneralSettings = GeneralSettings()
    rdb: RDBSettings = RDBSettings()
    # jwt: JWTSettings = JWTSettings()
    # mail: SMTPSettings = SMTPSettings()
    Idx: IdxSettings = IdxSettings()
    
settings = Settings()



"""
로깅 설정
"""
def setup_logging():
    logging.basicConfig(
        format="%(asctime)s:%(levelname)s:%(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p", 
        level=logging.DEBUG if settings.general.DEBUG else logging.INFO
    )

    _logger = logging.getLogger(__name__)
    _logger.info("Config 로드 완료")


