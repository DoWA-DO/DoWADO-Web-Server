from datetime import datetime, timedelta
from typing import Any, Dict, Tuple, Annotated
from fastapi import Depends, Request, HTTPException
from jose import jwt, ExpiredSignatureError, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from src.config.status import Status, ER
from src.config import settings
import logging

_logger = logging.getLogger(__name__)

SECRET_KEY = settings.jwt.JWT_SECRET_KEY
ALGORITHM = settings.jwt.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt.JWT_ACCESS_TOKEN_EXPIRE_MIN

# OAuth2PasswordBearer 설정
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scopes={"student": "Access as student", "teacher": "Access as teacher"}
)

# JWT, 패스워드 해싱 설정 : bcrypt 알고리즘을 사용하여 비밀번호 해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Claims:
    """ 토큰에 저장될 데이터 모델 """
    def __init__(self, username: str, scope: str):
        self.username = username
        self.scope = scope

    def to_dict(self) -> Dict[str, Any]:
        """객체를 딕셔너리로 변환"""
        return {"username": self.username, "scope": self.scope}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Claims":
        """딕셔너리를 객체로 변환"""
        return cls(username=data.get("username"), scope=data.get("scope"))

class JWT:
    """ JWT (JSON Web Token) 관련 유틸리티 클래스 """
    @classmethod
    def decode(cls, token: str) -> Dict[str, Any]:
        """ JWT 디코드 - 토큰을 디코딩하여 데이터를 반환 """
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    @classmethod
    def encode(cls, data: Dict[str, Any]) -> str:
        """JWT 인코드 - 데이터를 인코딩하여 토큰을 생성"""
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    @classmethod
    def create_token(cls, claims: Dict[str, Any], expires_delta: timedelta = None) -> str:
        """토큰 생성 - 데이터를 인코딩하여 토큰을 생성"""
        to_encode = claims.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "sub": "access"})
        return cls.encode(to_encode)

    @classmethod
    def verify(cls, token: str) -> Claims:
        """토큰 검증 - 토큰이 유효한지 검증하고 클레임 정보를 반환"""
        try:
            to_decode = cls.decode(token)
            if "access" == to_decode.get("sub"):
                return Claims.from_dict(to_decode)
            raise HTTPException(status_code=401, detail="Invalid token")
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    
    @classmethod
    def get_claims(cls, request: Request) -> Claims:
        """요청에서 토큰을 추출하고 클레임 반환"""
        token = request.headers.get("Authorization").split(" ")[1]
        return cls.verify(token)
    
    
    @classmethod
    async def get_current_user(cls, token: Annotated[str, Depends(oauth2_scheme)]) -> Dict[str, str]:
        """현재 사용자 정보 반환 - 토큰을 사용하여 사용자 정보 추출"""
        try:
            payload = cls.decode(token)
            username: str = payload.get("username")
            scope: str = payload.get("scope")
            if username is None or scope is None:
                _logger.error(f"Token validation failed for token: {token}")
                raise HTTPException(
                    status_code=401,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            if scope not in ["student", "teacher"]:
                _logger.error(f"Invalid scope: {scope}")
                raise HTTPException(
                    status_code=401,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            _logger.info(f"Current user retrieved: {username}, scope: {scope}")
            return {"username": username, "scope": scope}
        except JWTError:
            _logger.error(f"Token decoding failed for token: {token}")
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

class Crypto:
    """비밀번호 해싱 및 검증 유틸리티 클래스"""
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증 - 입력한 비밀번호와 저장된 해시된 비밀번호를 비교"""
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """비밀번호 해싱 - 비밀번호를 해싱하여 저장할 수 있는 형태로 변환"""
        return pwd_context.hash(password)
