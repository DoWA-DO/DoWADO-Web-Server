"""
NOTE: 리펙토링 작업 전
"""
from src.config.dto import BaseDTO


class Token(BaseDTO): 
    access_token: str
    token_type: str
    username: str