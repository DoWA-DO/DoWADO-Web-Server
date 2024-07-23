from typing import Annotated
from fastapi import Form
from pydantic import BaseModel
from enum import Enum


class UserTypeInfo(str, Enum):
    student = 'student'
    teacher = 'teacher'

class Credentials(BaseModel):
    email: Annotated[str, Form(description="이메일")]
    password: Annotated[str, Form(description="비밀번호")]


class Token(BaseModel):
    access_token: str
    refresh_token: str
