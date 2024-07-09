"""
API 개발 시 참고 : API 호출 시 데이터 전달 양식 정의
"""
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

class keyChat(BaseDTO):
    chat_name: Annotated[Union[str, None], Form(description="학생 이름")]
"""
class UpdateChat(BaseDTO):
    chat_text: Annotated[Union[str, None], Form(description="대화 내용")] = 'text1'
    chat_job: Annotated[Union[str, None], Form(description="직업")] = 'job1'
    chat_date: Annotated[datetime, Field(description="대화 날짜")] 
"""
class CreateChat(keyChat):
    chat_text: Annotated[Union[str, None], Form(description="대화 내용")] = 'text1'
    chat_job: Annotated[Union[str, None], Form(description="직업")] = 'job1'
    chat_date: Annotated[datetime, Field(description="대화 날짜")]

class ReadChatInfo(CreateChat):
    ...