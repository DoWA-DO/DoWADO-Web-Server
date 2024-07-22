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
    school_id: Annotated[int | None, Form(description="학교 ID")] = None
    # user_type: Annotated[UserTypeInfo | None, Form(description='유저 타입(교직원, 학생)')]
    
    # @classmethod
    # def as_form(
    #     cls,
    #     user_type: UserTypeInfo = Form(...)
        
    # ) -> 'Credentials':
    #     return cls(user_type=user_type)

class Token(BaseModel):
    access_token: str
    refresh_token: str
