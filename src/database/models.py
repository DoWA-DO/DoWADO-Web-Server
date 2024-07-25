"""
데이터베이스 테이블에 매핑될 모델 정의(ORM Model)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


'''
학교 테이블
'''
class School(Base):
    __tablename__ = 'schools'
    
    school_id = Column(Integer, primary_key=True, autoincrement=True)
    school_name = Column(String(100), nullable=False, unique=True)
    school_address = Column(Text, nullable=True)

    teachers = relationship('UserTeacher', back_populates='school')
    students = relationship('UserStudent', back_populates='school')

'''
유저 테이블
'''
class UserTeacher(Base):
    __tablename__ = 'user_teachers'
    
    teacher_email = Column(String(50), primary_key=True, nullable=False)
    teacher_name = Column(String(50), nullable=False)
    teacher_password = Column(String(128), nullable=False)
    school_id = Column(Integer, ForeignKey('schools.school_id'), nullable=False)
    teacher_grade = Column(Integer, nullable=False)
    teacher_class = Column(Integer, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)  # 이메일 인증 여부 추가
    
    school = relationship('School', back_populates='teachers')
    students = relationship('UserStudent', back_populates='teacher')

class UserStudent(Base):
    __tablename__ = 'user_students'
    
    student_email = Column(String(50), primary_key=True, nullable=False)
    school_id = Column(Integer, ForeignKey('schools.school_id'), nullable=False)
    student_name = Column(String(50), nullable=False)
    student_password = Column(String(128), nullable=False)
    student_grade = Column(Integer, nullable=False)
    student_class = Column(Integer, nullable=False)
    student_number = Column(Integer, nullable=False)
    teacher_email = Column(String(50), ForeignKey('user_teachers.teacher_email'), nullable=True)
    
    school = relationship('School', back_populates='students')
    teacher = relationship('UserTeacher', back_populates='students')
    chat_logs = relationship('ChatLog', back_populates='student')
    

'''
진로 추천 챗봇
'''
class ChatLog(Base):
    __tablename__ = 'chat_logs'
    
    chat_session_id = Column(String(64), primary_key=True, nullable=False)
    chat_content = Column(JSON, nullable=False)
    chat_date = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    chat_status = Column(Boolean, default=False, nullable=False)  # False : 편집X(레포트 생성) / True: 편집O(레포트 미생성)
    student_email = Column(String(50), ForeignKey('user_students.student_email'), nullable=False)
    
    student = relationship('UserStudent', back_populates='chat_logs')
    report = relationship('ChatReport', uselist=False, back_populates='chat_log')
    
    
class ChatReport(Base):
    __tablename__ = 'chat_reports'
    
    report_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    report_job_category = Column(Text, nullable=True)
    report_job_info = Column(Text, nullable=True)
    report_major = Column(Text, nullable=True)
    chat_session_id = Column(String(64), ForeignKey('chat_logs.chat_session_id'), nullable=False)
    
    chat_log = relationship('ChatLog', back_populates='report')
    
    
'''
이메일 인증
'''
# src/database/models.py

class EmailVerification(Base):
    __tablename__ = 'email_verifications'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False, unique=True)
    verification_code = Column(String(10), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
