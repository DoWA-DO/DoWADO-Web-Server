#login_control.py

"""
API 개발 시 참고 : 프론트엔드에서 http 엔드포인트를 통해 호출되는 메서드
"""
# 기본적으로 추가
from fastapi import APIRouter, Depends, HTTPException
from src.core.status import Status, SU, ER
import logging
from datetime import timedelta, datetime

# (db 세션 관련)이후 삭제 예정, 개발을 위해 일단 임시로 추가
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Security
from jose import JWTError, jwt
from src.core.config import SECRET_KEY
# 호출할 모듈 추가

from src.api.v1.users.teacher.teacher_dao import pwd_context
from src.api.v1.login import login_dto, login_dao

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
# secret key 생성 : openssl rand -hex 32
ALGORITHM = "HS256"

# 로깅 및 라우터 객체 생성 - 기본적으로 추가
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/login", tags=["로그인"])
    
# 학생 로그인
@router.post(
    "/student", 
    summary="학생 로그인",
    description="- 학생 db에서 일치하는 email, password 확인 후 로그인",
    response_model=login_dto.Token,
    responses=Status.docs(SU.SUCCESS, ER.UNAUTHORIZED)
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: AsyncSession = Depends(get_db)):
    # check user and password
    user = await login_dao.get_student(db, form_data.username) # db에서 사용자 정보 가져옴 (list)
    if not user or not pwd_context.verify(form_data.password, user[0]): # db와 비교
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logging.info("비교 여부: %s", pwd_context.verify(form_data.password, user[0]))
    
    # make access token
    data = {
        "sub": user[1],
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    logger.info("----------로그인----------")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user[1]
    }
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

@router.get("/me", response_model=login_dto.Token)
async def read_users_me(current_user: str = Security(get_current_user)):
    return {
        "access_token": "example_access_token",
        "token_type": "bearer",
        "username": current_user
    }
    
# 선생님 로그인
@router.post(
    "/teacher",
    summary="선생님 로그인",
    description="- 선생님 db에서 일치하는 email, password 확인 후 로그인",
    response_model=login_dto.Token,
    responses=Status.docs(SU.SUCCESS, ER.UNAUTHORIZED)
)
async def login_teacher_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                         db: AsyncSession = Depends(get_db)):
    # check user and password
    user = await login_dao.get_teacher(db, form_data.username) # db에서 사용자 정보 가져옴 (list)
    if not user or not pwd_context.verify(form_data.password, user[0]): # db와 비교
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logging.info("비교 여부: %s", pwd_context.verify(form_data.password, user[0]))
    
    # make access token
    data = {
        "sub": user[1],
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    logger.info("----------로그인----------")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user[1]
    }
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username