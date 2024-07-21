from typing import Annotated
from fastapi import Form
from pydantic import BaseModel


class Credentials(BaseModel):
    email: Annotated[str, Form(description="이메일")]
    password: Annotated[str, Form(description="비밀번호")]
    school_id: Annotated[int | None, Form(description="학교 ID")] = None

class Token(BaseModel):
    access_token: str
    refresh_token: str
