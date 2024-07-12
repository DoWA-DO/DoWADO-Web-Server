"""
데이터베이스 테이블에 매핑될 모델 정의(ORM Model)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

'''
유저 테이블
'''
class UserTeacher(Base):
    __tablename__ = 'user_teachers'
    
    teacher_email = Column(String(30), primary_key=True, nullable=False)
    teacher_name = Column(String(30), nullable=True)
    teacher_password = Column(String(128), nullable=True)
    teacher_school = Column(Text, nullable=True)
    teacher_grade = Column(Integer)
    teacher_class = Column(Integer)
    teacher_profile_img = Column(Text)
    
    students = relationship('UserStudent', back_populates='teacher')


class UserStudent(Base):
    __tablename__ = 'user_students'
    
    student_email = Column(String(30), primary_key=True, nullable=False)
    student_school = Column(Text, nullable=True)
    student_name = Column(String(30), nullable=True)
    student_password = Column(String(128), nullable=True)
    student_grade = Column(Integer)
    student_class = Column(Integer)
    student_number = Column(Integer)
    student_profile_img = Column(Text)
    teacher_email = Column(String(30), ForeignKey('user_teachers.teacher_email'))
    
    teacher = relationship('UserTeacher', back_populates='students')
    chat_logs = relationship('ChatLog', back_populates='student')
    

'''
진로 추천 챗봇
'''
class ChatLog(Base):
    __tablename__ = 'chat_logs'
    
    chat_session_id = Column(String(30), primary_key=True, nullable=False)
    chat_content = Column(JSON)
    chat_date = Column(DateTime(timezone=True))
    chat_status = Column(Integer)
    student_email = Column(String(30), ForeignKey('user_students.student_email'))
    
    student = relationship('UserStudent', back_populates='chat_logs')
    report = relationship('ChatReport', uselist=False, back_populates='chat_log')
    
    
class ChatReport(Base):
    __tablename__ = 'chat_reports'
    
    report_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    report_1st = Column(String(30))
    report_2nd = Column(String(30))
    report_3rd = Column(String(30))
    report_info = Column(Text)
    chat_session_id = Column(String(30), ForeignKey('chat_logs.chat_session_id'))
    
    chat_log = relationship('ChatLog', back_populates='report')