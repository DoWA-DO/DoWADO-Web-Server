from datetime import timedelta, datetime
from typing import Annotated, Any, Callable, Tuple
from fastapi import Depends, Request, HTTPException
from jose import ExpiredSignatureError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from src.config import settings
import logging

logger = logging.getLogger(__name__)

class Claims(BaseModel):
    user_id: str
    email: str
    school_id: int | None = None
    role: str | None = None

    class Config:
        orm_mode = True
        from_attributes = True

    @classmethod
    def parse_obj(cls, obj):
        if isinstance(obj, dict) and 'role' in obj and isinstance(obj['role'], dict):
            obj['role'] = str(obj['role']) # role 필드를 문자열로 변환
        return super().parse_obj(obj)

class JWT:
    ALGORITHM = "HS256"
    SECRET_KEY = settings.jwt.JWT_SECRET_KEY  # Replace with your actual secret key

    @classmethod
    def decode(cls, token: str) -> dict[str, Any]:
        return jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])

    @classmethod
    def encode(cls, data: dict) -> str:
        return jwt.encode(data, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def _verify(cls, sub: str, request: Request, token: str):
        if token:
            try:
                to_decode = cls.decode(token)
                if sub == to_decode.get("sub"):
                    request.state.claims = Claims.parse_obj(to_decode)
                    logger.info(f"=>> Claims set in request state: {request.state.claims}")
                else:
                    raise HTTPException(status_code=401, detail="Invalid token")
            except ExpiredSignatureError as err:
                raise HTTPException(status_code=401, detail="Token expired") from err
            except Exception as err:
                raise HTTPException(status_code=401, detail="Invalid token") from err
        else:
            raise HTTPException(status_code=401, detail="Token not found", headers={"WWW-Authenticate": "Bearer"})

    @classmethod
    def verify(cls, request: Request, token: Annotated[str, Depends]):
        cls._verify("access", request, token)
        if not hasattr(request.state, "claims"):
            raise HTTPException(status_code=401, detail="Claims not found")
    @classmethod
    def verify_by_refresh(cls, request: Request, token: Annotated[str, Depends]):
        cls._verify("refresh", request, token)
        if not hasattr(request.state, "claims"):
            raise HTTPException(status_code=401, detail="Claims not found")

    @classmethod
    def get_claims(cls, name: str | None = None) -> Callable[..., Claims]:
        def _get_claims(request: Request) -> Claims:
            if not hasattr(request.state, "claims"):
                raise HTTPException(status_code=401, detail="Claims not found")
            if name:
                return getattr(request.state.claims, name)
            return request.state.claims

        return _get_claims

    @classmethod
    def _create_token(cls, sub: str, claims: dict, expires_delta: timedelta) -> str:
        to_encode = {"sub": sub}
        to_encode.update(claims)
        to_encode.update({"iat": datetime.utcnow()})
        to_encode.update({"exp": datetime.utcnow() + expires_delta})
        # role 필드를 문자열로 변환
        if isinstance(to_encode.get("role"), dict):
            to_encode["role"] = str(to_encode["role"])
        logger.debug(f"=>> Token claims before encoding: {to_encode}")
        return cls.encode(to_encode)

    @classmethod
    def create_token(cls, claims: dict) -> Tuple[str, str]:
        access_token = cls._create_token(sub="access", claims=claims, expires_delta=timedelta(minutes=15))
        refresh_token = cls._create_token(sub="refresh", claims=claims, expires_delta=timedelta(days=30))
        return access_token, refresh_token

class Crypto:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password):
        return cls.pwd_context.hash(password)
