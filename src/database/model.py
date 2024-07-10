"""
데이터베이스 테이블에 매핑될 모델 정의(ORM Model)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 채팅 테이블
class Chat(Base):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_user = Column(Text, primary_key=True) # 학생 이름
    chat_text = Column(Text, nullable=True) # 대화 내용
    created_at =  Column(DateTime, nullable=False)
    
# 교원 테이블    
class Teacher(Base):
    __tablename__ = "teacher"
    
    teacher_email = Column(String, primary_key=True) # 교원 메일
    teacher_auth = Column(Boolean, default = False, nullable = False) # 교원 인증 여부
    teacher_password = Column(String, nullable=False) # 교원 비밀번호
    teacher_name = Column(String, unique=True, nullable=False) # 교원 이름
    teacher_schoolname = Column(String, nullable=False) # 교원 학교 이름
    #teacher_num = Column(int, nullable=False) # 교원 학년/반/00
    #teacher_picture은 기본적으로는 False로 제공, 이후 S3에 해당 계정의 사진이 올라갔는지를 확인하고 True로 바꾸는 로직 필요?
    #teacher_picture = True면 aws S3에 저장된 사진을 불러오는 로직 필요할것 으로 예상함. - TODO
    #teacher_picture = Column(Boolean, default = False, nullable = False)