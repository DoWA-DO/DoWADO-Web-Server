# 기본적으로 추가
from typing import Optional, Annotated
from datetime import datetime, timezone
from fastapi import Depends, Form, Path
from pydantic import Field
from src.database.dto import BaseDTO
from typing import Union


# - 개발하려는 API의 목적에 맞게 클래스 작성
# - 중복되는 부분은 상속받아서 중복 코드 최소화하기
# - src/var/model.py에 데이터베이스에 생성하고자하는 테이블 먼저 선언 후, 해당 클래스 참고하여 dto를 작성하면 편함
# - 데이터 전달 객체를 사용하는 API의 목적에 따라서 클래스명 작성
#   1) Read, Create, Update, Delete 중 1택
#   2) 목적에 따라 클래스명 원하는 대로 선언(컨벤션에 맞춰 작성할 것, 대소문자 유의)

class keyTeacher(BaseDTO):
    teacher_email: Annotated[Union[str, None], Form(description="교원 메일")]

class UpdateTeacher(BaseDTO):
    teacher_password: Annotated[Union[str, None], Form(description="교원 비밀번호")] 
    teacher_name: Annotated[Union[str, None], Form(description="교원 이름")] 
    teacher_schoolname: Annotated[Union[str, None], Field(description="교원 학교 이름")] 

class CreateTeacher(keyTeacher, UpdateTeacher):
    teacher_auth: Annotated[Union[bool, None], Form(description="메일 인증 여부")]
    ...

class ReadTeacherInfo(CreateTeacher):
    ...