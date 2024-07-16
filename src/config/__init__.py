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
    DB_PROTOCAL: str = "postgresql+asyncpg"  # 환경변수에 저장해야 함
    DB_USERNAME: str = "dowado"
    DB_PASSWORD: str = SecretStr
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
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

class Settings(BaseSettings):
    general: GeneralSettings = GeneralSettings()
    rdb: RDBSettings = RDBSettings()
    # jwt: JWTSettings = JWTSettings()
    # mail: SMTPSettings = SMTPSettings()
    
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


