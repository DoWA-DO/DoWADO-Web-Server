from typing import Annotated
from fastapi import Form
from src.config.dto import BaseDTO

class Credentials(BaseDTO):
    username: Annotated[str, Form(description="사용자 이름")]
    password: Annotated[str, Form(description="사용자 비밀번호")]
    scope: Annotated[str, Form(description="사용자 범위 (학생 또는 교사)")]

class Token(BaseDTO):
    access_token: str
    token_type: str
    username: str
