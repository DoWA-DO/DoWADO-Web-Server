from typing import Optional
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from src.config.status import ER
from src.api.auth.login_dao import get_teacher, get_student, get_teacher_role, get_student_role
from src.config.security import Claims, Crypto, JWT
from src.api.auth.login_dto import Credentials, Token, UserTypeInfo
import logging


logger = logging.getLogger(__name__)

async def login(credentials: Credentials, user_type: Optional[UserTypeInfo] = None) -> Token:
    """
    사용자 로그인 처리 함수.
    이메일을 통해 교사인지 학생인지 식별한 후, 비밀번호를 검증하고 토큰을 발행합니다.
    
    :param credentials: 사용자의 이메일과 비밀번호가 포함된 Credentials 객체
    :return: 액세스 토큰과 리프레시 토큰을 포함한 Token 객체
    """
    user = None
    password = None
    role = user_type.value
    user_id = None
    school_id = None
    
    try:
        if role == 'teacher':
            user = await get_teacher(credentials.email)
            if user:
                password = user.teacher_password
                user_id = user.teacher_email
                school_id = user.school_id
            else:
                logger.error(f"No teacher found for email: {credentials.email}")
                raise HTTPException(status_code=404, detail="User not found")
        elif role == 'student':
            user = await get_student(credentials.email)
            if user:
                password = user.student_password
                user_id = user.student_email
                school_id = user.school_id
            else:
                logger.error(f"No student found for email: {credentials.email}")
                raise HTTPException(status_code=404, detail="User not found")
        else:
            logger.error(f"Invalid user type: {role}")
            raise HTTPException(status_code=400, detail="Invalid user type")
    
    
        # 사용자 비밀번호 검증
        if not Crypto.verify_password(credentials.password, password):
            logger.error("Invalid password")
            raise ER.INVALID_PASSWORD
    
        # 사용자 정보를 바탕으로 JWT Claims 생성
        claims = {
            "user_id": user_id,
            "email": credentials.email,
            "school_id": school_id,
            "role": role,
        }
    
        # Claims 객체를 JSON으로 인코딩
        encoded_claims = jsonable_encoder(claims)
    
    
        # 토큰 발행
        access_token, refresh_token = JWT.create_token(claims=encoded_claims)
        return Token(access_token=access_token, refresh_token=refresh_token)
    except HTTPException as e:
        logger.error(f"Login error: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected login error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def login_as_school(claims: dict, user_type: str) -> Token:
    """
    학교 권한 확인 후 토큰을 발행하는 함수.
    사용자가 교사인지 학생인지 식별한 후, 적절한 권한을 부여합니다.
    
    :param claims: 사용자 정보가 포함된 Claims 객체
    :return: 액세스 토큰과 리프레시 토큰을 포함한 Token 객체
    """
    # 이메일 주소를 통해 교사와 학생을 구분하여 적절한 DAO 함수를 호출
    if user_type == 'teacher':
        user_role = await get_teacher_role(claims['school_id'], claims['email'])
    else:
        user_role = await get_student_role(claims['school_id'], claims['email'])
    
    # 권한 정보를 Claims에 추가
    claims['role'] = user_role
    
    # 토큰 발행
    encoded_claims = jsonable_encoder(claims)
    access_token, refresh_token = JWT.create_token(claims=encoded_claims)
    return Token(access_token=access_token, refresh_token=refresh_token)


async def refresh(claims: Claims) -> Token:
    """
    리프레시 토큰을 사용하여 새로운 액세스 토큰과 리프레시 토큰을 발행하는 함수.
    
    :param claims: 사용자 정보가 포함된 Claims 객체
    :return: 액세스 토큰과 리프레시 토큰을 포함한 Token 객체
    """
    claims_dict = {
        "user_id": claims.user_id,
        "email": claims.email,
        "school_id": claims.school_id,
        "role": str(claims.role),
    }
    encoded_claims = jsonable_encoder(claims_dict)
    access_token, refresh_token = JWT.create_token(claims=encoded_claims)
    return Token(access_token=access_token, refresh_token=refresh_token)
