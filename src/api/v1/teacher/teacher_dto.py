"""
API 개발 시 참고 : API 호출 시 데이터 전달 양식 정의
"""
# 기본적으로 추가
from typing import Optional, Annotated
from datetime import datetime, timezone
from fastapi import Depends, Form, Path
from pydantic import Field
from src.database.dto import BaseDTO

class keyTeacher(BaseDTO):
    teacher_email: Annotated[str | None, Form(description="교원 이메일")]


class UpdateTeacher(BaseDTO):
    teacher_password: Annotated[str | None, Form(description="변경할 비밀번호")]
    teacher_name: Annotated[str | None, Field(description="변경할 이름")]
    teacher_schoolname: Annotated[str | None, Field(description="변경할 학교 이름")]

class CreateTeacher(keyTeacher, UpdateTeacher):
    teacher_email: Annotated[str | None, Form(description="교원 이메일")]
    teacher_password: Annotated[str | None, Form(description="계정 비밀번호")]
    teacher_name: Annotated[str | None, Field(description="교원 이름")]
    teacher_schoolname: Annotated[str | None, Field(description="학교 이름")]


class ReadTeacherInfo(CreateTeacher):
    teacher_email: Annotated[str | None, Form(description="교원 이메일")]
    teacher_password: Annotated[str | None, Form(description="계정 비밀번호")]
    teacher_name: Annotated[str | None, Field(description="교원 이름")]
    teacher_schoolname: Annotated[str | None, Field(description="학교 이름")]
    teacher_auth: Annotated[bool | None, Field(description="인증 여부")]
    #teacher_picture = True면 S3에 저장된 사진을 불러오게 해야 함.
    teacher_picture: Annotated[bool | None, Field(description="교원 사진 여부")]

    
class DeleteTeacher(BaseDTO):
    teacher_id: Annotated[str, Form(description="삭제할 교원 이메일")]