from typing import Annotated, Union
from pydantic import EmailStr, Field, BaseModel, ConfigDict, model_validator
from fastapi import Form
from src.config.dto import BaseDTO

class KeyStudent(BaseDTO):
    student_email: Annotated[Union[EmailStr, None], Form(description="학생 메일")]

class UpdateStudent(BaseDTO):
    student_grade: Annotated[Union[int, None], Form(description="학생 학년")]
    student_class: Annotated[Union[int, None], Form(description="학생 반")]
    student_number: Annotated[Union[str, None], Form(description="학생 번호")]
    student_name: Annotated[Union[str, None], Form(description="학생 이름")]
    student_password: Annotated[Union[str, None], Form(description="학생 비밀번호")]
    student_new_password: Annotated[Union[str, None], Form(description="학생 신규 비밀번호")]

class CreateStudent(KeyStudent):
    school_id: Annotated[Union[int, None], Form(description="학교 ID")]
    student_grade: Annotated[Union[int, None], Form(description="학생 학년")]
    student_class: Annotated[Union[int, None], Form(description="학생 반")]
    student_number: Annotated[Union[int, None], Form(description="학생 번호")]
    student_name: Annotated[Union[str, None], Form(description="학생 이름")]
    student_password: Annotated[Union[str , None], Form(description="학생 비밀번호")]
    student_password2: Annotated[Union[str, None], Form(description="학생 비밀번호 확인")]
    teacher_email: Annotated[Union[EmailStr, None], Form(description="선생님 이메일")]  # 필드 이름 수정

    @model_validator(mode='before')
    @classmethod
    def not_empty(cls, values):
        required_fields = ['student_email', 'student_password', 'student_password2', 'student_name', 'teacher_email']
        for field in required_fields:
            if not values.get(field) or not str(values.get(field)).strip():
                raise ValueError(f'{field}은(는) 빈 값일 수 없습니다.')
        return values

    @model_validator(mode='before')
    @classmethod
    def check_integer(cls, values):
        integer_fields = ['student_grade', 'student_class', 'student_number']
        for field in integer_fields:
            if values.get(field) is not None and not isinstance(values.get(field), int):
                raise ValueError(f'{field}은(는) 정수 값이어야 합니다.')
        return values

    @model_validator(mode='before')
    @classmethod
    def passwords_match(cls, values):
        if values.get('student_password') != values.get('student_password2'):
            raise ValueError('비밀번호가 일치하지 않습니다')
        return values

class ReadStudentInfo(BaseDTO):
    school_id: int
    student_name: str
    student_email: str
    student_grade: int
    student_class: int
    student_number: int
    teacher_email: str  # 필드 이름 수정

class SchoolDTO(BaseDTO):
    school_id: int
    school_name: str
