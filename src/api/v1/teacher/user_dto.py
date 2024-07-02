"""
API 개발 시 참고 : API 호출 시 데이터 전달 양식 정의
"""
# 기본적으로 추가
from typing import Optional, Annotated
from datetime import datetime, timezone
from fastapi import Depends, Form, Path
from pydantic import Field
from src.database.dto import BaseDTO

class Teacherkey(BaseDTO):
    teacher_email: Annotated[str | None, Form(description="교원 이메일")]


class Teacherupdate(BaseDTO):
    teacher_password: Annotated[str | None, Form(description="예제 내용1_Form")] = 'sample1'
    teacher_name: Annotated[str | None, Field(description="예제 내용2_Field")] = 'sample2'


class CreateExample(keyExample, UpdateExample):
    ...


class ReadExampleInfo(CreateExample):
    ...

    
class DeleteExample(BaseDTO):
    example_id: Annotated[str, Form(description="삭제할 예제 id")]