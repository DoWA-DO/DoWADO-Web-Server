# su_dto.py

from typing import Annotated, Union
from pydantic import BaseModel, EmailStr, Field, validator

class KeyTeacher(BaseModel):
    teacher_email: Annotated[Union[EmailStr, None], Field(description="교원 메일")]

class UpdateTeacher(BaseModel):
    teacher_password: Annotated[Union[str, None], Field(description="교원 비밀번호")]
    
class ReadTeacherInfo(KeyTeacher, UpdateTeacher):
    pass

class CreateTeacher(KeyTeacher, UpdateTeacher):
    teacher_name: Annotated[Union[str, None], Field(description="교원 이름")]
    teacher_school: Annotated[Union[str, None], Field(description="교원 학교 이름")]
    teacher_password2: Annotated[Union[str, None], Field(description="교원 비밀번호 확인")]
    teacher_grade: Annotated[Union[int, None], Field(description="교원 학년")]
    teacher_class: Annotated[Union[int, None], Field(description="교원 반")]
    

    @validator('teacher_email', 'teacher_password', 'teacher_password2', 'teacher_name', 'teacher_school')
    def not_empty(cls, v):
        if not v or not str(v).strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @validator('teacher_grade', 'teacher_class')
    def check_integer(cls, v):
        if v is not None and not isinstance(v, int):
            raise ValueError('정수 값이 필요합니다.')
        return v

    @validator('teacher_password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'teacher_password' in values and v != values['teacher_password']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v
    
class KeyStudent(BaseModel):
    student_email: Annotated[Union[EmailStr, None], Field(description="학생 메일")]

class UpdateStudent(BaseModel):
    student_password: Annotated[Union[str, None], Field(description="학생 비밀번호")]

class ReadStudentInfo(KeyStudent, UpdateStudent):
    pass

class CreateStudent(KeyStudent, UpdateStudent):
    student_school: Annotated[Union[str, None], Field(description="학생 학교 이름")]
    student_name: Annotated[Union[str, None], Field(description="학생 이름")]
    student_password2: Annotated[Union[str, None], Field(description="학생 비밀번호 확인")]
    student_grade: Annotated[Union[int, None], Field(description="학생 학년")]
    student_class: Annotated[Union[int, None], Field(description="학생 반")]
    student_number: Annotated[Union[int, None], Field(description="학생 번호")]
    student_teacher_email: Annotated[Union[EmailStr, None], Field(description="담당 선생님 메일")]

    @validator('student_email', 'student_password', 'student_password2', 'student_name', 'student_school', 'student_teacher_email')
    def not_empty(cls, v):
        if not v or not str(v).strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @validator('student_grade', 'student_class', 'student_number')
    def check_integer(cls, v):
        if v is not None and not isinstance(v, int):
            raise ValueError('정수 값이 필요합니다.')
        return v

    @validator('student_password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'student_password' in values and v != values['student_password']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v