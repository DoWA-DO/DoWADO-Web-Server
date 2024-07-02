"""
데이터베이스 테이블에 매핑될 모델 정의(ORM Model)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

'''
테스트용 테이블
'''
class Job(Base): 
    __tablename__ = "example"

    example_id = Column(String, primary_key=True)
    example_name = Column(Text, nullable=True)
    example_comm1 = Column(Text, nullable=True)
    example_comm2 = Column(Text, nullable=True)

# 채팅 테이블
class Chat(Base):
    __tablename__ = "chat"

    chat_name = Column(Text, primary_key=True) # 학생 이름
    chat_text = Column(Text, nullable=True) # 대화 내용
    chat_job = Column(Text, nullable=True) # 직업 (추천 결과)
    chat_date = Column(TIMESTAMP(timezone=True), nullable=False) # 날짜