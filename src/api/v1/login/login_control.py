from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Security
from src.core.status import Status, SU, ER
import logging
from datetime import timedelta, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from src.core.config import SECRET_KEY
from src.api.v1.users.teacher.teacher_dao import pwd_context
from src.api.v1.login import login_dto, login_dao
from src.api.v1.login.login_dto import Token

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
ALGORITHM = "HS256"

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/login", tags=["로그인"])

STUDENT_SCOPE = "student"
TEACHER_SCOPE = "teacher"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/login/student",
    scopes={"student": "Access as student", "teacher": "Access as teacher"}
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        scope: str = payload.get("scope")
        if username is None or scope is None:
            logger.error(f"Token validation failed for token: {token}")
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if scope == STUDENT_SCOPE:
            tokenUrl = "/api/v1/login/student"
        elif scope == TEACHER_SCOPE:
            tokenUrl = "/api/v1/login/teacher"
        else:
            logger.error(f"Invalid scope: {scope}")
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.info(f"Current user retrieved: {username}, scope: {scope}")
        return {"username": username, "scope": scope, "tokenUrl": tokenUrl}
    
    except JWTError:
        logger.error(f"Token decoding failed for token: {token}")
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def authenticate_student_user(username: str, password: str, db: AsyncSession):
    user = await login_dao.get_student_user(db, username)
    if not user or not pwd_context.verify(password, user[0]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info(f"Student user authenticated: {username}")
    return user[1]

async def authenticate_teacher_user(username: str, password: str, db: AsyncSession):
    user = await login_dao.get_teacher_user(db, username)
    if not user or not pwd_context.verify(password, user[0]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info(f"Teacher user authenticated: {username}")
    return user[1]

@router.post(
    "/student",
    summary="학생 로그인",
    description="- 학생 db에서 일치하는 email, password 확인 후 로그인",
    response_model=login_dto.Token,
    responses=Status.docs(SU.SUCCESS, ER.UNAUTHORIZED)
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    username = await authenticate_student_user(form_data.username, form_data.password, db)
    data = {
        "sub": username,
        "scope": STUDENT_SCOPE,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    logger.info("----------로그인----------")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": username
    }

@router.post(
    "/teacher",
    summary="선생님 로그인",
    description="- 선생님 db에서 일치하는 email, password 확인 후 로그인",
    response_model=login_dto.Token,
    responses=Status.docs(SU.SUCCESS, ER.UNAUTHORIZED)
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    username = await authenticate_teacher_user(form_data.username, form_data.password, db)
    data = {
        "sub": username,
        "scope": TEACHER_SCOPE,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    logger.info("----------로그인----------")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": username
    }

@router.get(
    "/me",
    summary="사용자 정보 조회",
    description="- 토큰 정보를 이용하여 사용자 정보 조회",
    response_model=login_dto.Token,
)
async def read_users_me(current_user: str = Security(get_current_user)):
    return {
        "access_token": "example_access_token",
        "token_type": "bearer",
        "username": current_user['username'],
        "tokenUrl": current_user['tokenUrl']
    }
