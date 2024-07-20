from src.config.status import ER
from src.api.auth import login_dao
from src.config.security import Claims, Crypto, JWT
from src.api.auth.login_dto import Credentials, Token

async def login(credentials: Credentials) -> Token:
    """사용자 인증 및 토큰 발행"""
    if credentials.scope == "student":
        user = await login_dao.get_student_user(credentials.username)
        password_field = user.student_password
    elif credentials.scope == "teacher":
        user = await login_dao.get_teacher_user(credentials.username)
        password_field = user.teacher_password
    else:
        raise ER.INVALID_SCOPE
    
    if not Crypto.verify_password(credentials.password, password_field):
        raise ER.INVALID_PASSWORD
    
    claims = Claims(username=credentials.username, scope=credentials.scope)
    access_token = JWT.create_token(claims.to_dict())
    return Token(access_token=access_token, token_type="bearer", username=credentials.username)

async def refresh(claims: Claims) -> Token:
    """리프레시 토큰으로 액세스 토큰 재발급"""
    new_claims = Claims(username=claims.username, scope=claims.scope)
    access_token = JWT.create_token(new_claims.to_dict())
    return Token(access_token=access_token, token_type="bearer", username=claims.username)
