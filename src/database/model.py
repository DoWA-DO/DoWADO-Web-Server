"""
데이터베이스 테이블에 매핑될 모델 정의(ORM Model)
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

Base = declarative_base()

# 학생 테이블    
class UserStudent(Base):
    __tablename__ = "user_student"
    
    student_email = Column(Text, primary_key=True, unique=True) # 학생 메일
    student_name = Column(String, nullable=False) # 학생 이름
    student_school = Column(String, nullable=False) # 학생 학교 이름
    student_password = Column(String, nullable=False) # 학생 비밀번호
    student_grade = Column(Integer, nullable=False) # 학생 학년
    student_class = Column(Integer, nullable=False) # 학생 반
    student_number = Column(Integer, nullable=False) # 학생 번호
    student_teacher_email = Column(Text, ForeignKey('user_teacher.teacher_email')) # 담당 교사 이메일
    
# 교원 테이블    
class UserTeacher(Base):
    __tablename__ = "user_teacher"
    
    teacher_email = Column(Text, primary_key=True, unique=True) # 교원 메일
    teacher_name = Column(String, nullable=False) # 교원 이름
    teacher_password = Column(String, nullable=False) # 교원 비밀번호
    teacher_school = Column(String, nullable=False) # 교원 학교 이름
    teacher_grade = Column(Integer, nullable=False) # 교원 학년
    teacher_class = Column(Integer, nullable=False) # 교원 반
    
    students = relationship("UserStudent", backref="teacher")
    
# 채팅 테이블
class ChatLog(Base):
    __tablename__ = "chat_log"
    
    id = Column(Integer, primary_key=True, autoincrement=True) # 채팅 고유 번호
    chat_student_email  = Column(Text, ForeignKey('user_student.student_email'), nullable=False) # 학생 메일
    chat_content  = Column(Text, nullable=False) # 학생이 보낸 대화 
    chat_response = Column(Text, nullable=False) # 챗봇으로부터 받은 답변
    chat_date = Column(DateTime, default=func.now()) # 대화 종료 일시 자동 기록
    chat_status =  Column(Integer, default=0) # 리포트 생성 여부 (0:미생성, 1:생성)
    
    student = relationship("UserStudent", backref="chat_logs")
    
# 레포트 테이블
class Report(Base):
    __tablename__ = "report"
    
    id = Column(Integer, primary_key=True, autoincrement=True) # 레포트 고유 번호
    chat_log_id =  Column(Integer, ForeignKey('chat_log.id')) # 채팅 고유 번호
    report_1st = Column(String, nullable=False) # 직무 1순위
    report_2nd =Column(String, nullable=False) # 직무 2순위
    report_3rd = Column(String, nullable=False) # 직무 3순위
    report_info =  Column(Text, nullable=False) # 직업 설명