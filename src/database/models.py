"""
데이터베이스 테이블에 매핑될 모델 정의(ORM Model)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

'''
테스트용 테이블
'''
class Example(Base):
    __tablename__ = "example"

    example_id = Column(String, primary_key=True)
    example_name = Column(Text, nullable=True)
    example_comm1 = Column(Text, nullable=True)
    example_comm2 = Column(Text, nullable=True)
    
'''
교원용 테이블
'''
class Teacher(Base):
    __tablename__ = "teacher"
    
    teacher_email = Column(String, primary_key=True)
    teacher_auth = Column(Boolean, nullable=False)
    teacher_password = Column(String, nullable=False)
    teacher_name = Column(String, nullable=False)
    