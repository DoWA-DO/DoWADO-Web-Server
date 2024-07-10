# super_teacher_dto.py

# 기본적으로 추가
from typing import Annotated
from fastapi import Form
from pydantic import Field
from src.database.dto import BaseDTO
from typing import Union
from pydantic import field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo

# - 개발하려는 API의 목적에 맞게 클래스 작성
# - 중복되는 부분은 상속받아서 중복 코드 최소화하기
# - src/var/model.py에 데이터베이스에 생성하고자하는 테이블 먼저 선언 후, 해당 클래스 참고하여 dto를 작성하면 편함
# - 데이터 전달 객체를 사용하는 API의 목적에 따라서 클래스명 작성
#   1) Read, Create, Update, Delete 중 1택
#   2) 목적에 따라 클래스명 원하는 대로 선언(컨벤션에 맞춰 작성할 것, 대소문자 유의)

class keyTeacher(BaseDTO):
    teacher_email: Annotated[Union[EmailStr, None], Form(description="교원 메일")] # EmailStr(이메일 형식 확인)

class UpdateTeacher(BaseDTO):
    teacher_password: Annotated[Union[str, None], Form(description="교원 비밀번호")] 
    teacher_name: Annotated[Union[str, None], Form(description="교원 이름")] 
    teacher_schoolname: Annotated[Union[str, None], Field(description="교원 학교 이름")] 
    teacher_auth: Annotated[Union[bool, None], Form(description="메일 인증 여부")]
    # 선생 학교/반을 입력시켜 선생마다 학생 db 관리 쉽게 카테고리화 (ex. 20100 2학년 1반 선생님) 
    # 선생마다 학생 table 생성하면 자원 낭비 아닌가 싶어서 위에처럼 선생은 00번에 저장
    #teacher_grade: Annotated[Union[int, None], Form(description="학년")] 
    #teacher_class: Annotated[Union[int, None], Form(description="반")] 

class ReadTeacherInfo(keyTeacher,UpdateTeacher):
    ...
    
class CreateTeacher(keyTeacher, UpdateTeacher):
    teacher_password2: Annotated[Union[str, None], Form(description="교원 비밀번호 확인")]
    
    @field_validator('teacher_email', 'teacher_password', 'teacher_password2', 'teacher_name', 'teacher_schoolname')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    
    @field_validator('teacher_password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'teacher_password' in info.data and v != info.data['teacher_password']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v