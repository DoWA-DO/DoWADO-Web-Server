"""
API 개발 시 참고 : API 호출 시 데이터 전달 양식 정의
"""
#이 페이지에 super_teacher 권한을 정리해서 RUD 반영, 아마 Create는 안하는게 맞을듯. - TODO

# 기본적으로 추가
from typing import Optional, Annotated
from datetime import datetime, timezone
from fastapi import Depends, Form, Path
from pydantic import Field
from src.database.dto import BaseDTO

class keySuperTeacher(BaseDTO):
    super_teacher_email: Annotated[str | None, Form(description="교원 이메일")]