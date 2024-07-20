"""
계정 권한 인증 API (학생, 교사 로그인)
"""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Security, Request
from src.config.status import Status, SU, ER
from src.config import settings
from src.config.security import JWT, Claims, Crypto, oauth2_scheme
from src.api.auth import login_service
from src.api.auth.login_dto import Credentials, Token
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["회원 권한 인증(로그인) API"], responses=Status.docs(SU.SUCCESS))

@router.post(
    "/login",
    summary="사용자 인증 후 토큰 발행",
    description=f"- 로그인 성공 시 토큰 발행\n- 토큰 만료 시간은 {settings.jwt.JWT_ACCESS_TOKEN_EXPIRE_MIN}분",
    response_model=Token,
    responses=Status.docs(ER.NOT_FOUND, ER.INVALID_PASSWORD),
)
async def login(credentials: Annotated[Credentials, Depends()]) -> Token:
    token = await login_service.login(credentials)
    return token

@router.get(
    "/verify",
    summary="토큰 유효성 확인",
    description="- 토큰이 유효하지 않으면 에러 반환",
    dependencies=[Depends(JWT.verify)],
    responses=Status.docs(ER.INVALID_TOKEN, ER.NOT_TOKEN),
)
async def verify():
    return SU.SUCCESS

@router.get(
    "/refresh",
    summary="리프레시 토큰으로 토큰 재발급",
    description=f"- 토큰 만료 시간은 {settings.jwt.JWT_ACCESS_TOKEN_EXPIRE_MIN}분",
    response_model=Token,
    responses=Status.docs(ER.INVALID_TOKEN, ER.NOT_TOKEN),
)
async def refresh(request: Request) -> Token:
    claims = JWT.get_claims(request)
    new_token = await login_service.refresh(claims)
    return new_token

@router.get(
    "/me",
    summary="사용자 정보 조회",
    description="- 토큰 정보를 이용하여 사용자 정보 조회",
    response_model=dict,
    dependencies=[Depends(JWT.verify)],
)
async def read_users_me(current_user: Annotated[dict, Depends(JWT.get_current_user)]) -> dict:
    return {"username": current_user['username'], "scope": current_user['scope']}
