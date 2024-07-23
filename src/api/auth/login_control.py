"""
계정 권한 관련(로그인) API
"""
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Path
from src.config.security import JWT, Claims
from src.api.auth import login_service
from src.api.auth.login_dto import Credentials, Token, UserTypeInfo
from src.config.status import ER, SU, Status
from fastapi import Form
import logging


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["계정 권한 관련(로그인) API"], responses=Status.docs(SU.SUCCESS))


@router.post(
    "/login",
    summary="학생/교직원 공통 로그인 : 사용자 인증 후 토큰 발행",
    description="- 로그인 성공 시 토큰이 발행됩니다.",
    response_model=Token,
    responses=Status.docs(ER.INVALID_REQUEST, ER.INVALID_TOKEN, ER.UNAUTHORIZED),
)
async def login(
    email: Annotated[str, Form(description="이메일")],
    password: Annotated[str, Form(description="비밀번호")], # credentials: Annotated[Credentials, Depends()],
    user_type: Annotated[UserTypeInfo, Form()]  # 사용자 유형을 명시적으로 받도록 설정
) -> Token:
    credentials = Credentials(email=email, password=password)
    logger.info(f'=>> [control] 데이터입력 >> email, pw : {credentials}, type : {user_type}')
    token = await login_service.login(credentials, user_type)
    return token


@router.post(
    "/refresh",
    summary="리프레시 토큰으로 새로운 토큰 재발급",
    description="- 로그인 상태를 유지하고자 할 때 해당 API 호출함.",
    dependencies=[Depends(JWT.verify_by_refresh)],
    response_model=Token,
    responses=Status.docs(ER.INVALID_TOKEN, ER.UNAUTHORIZED, ER.NOT_FOUND),
)
async def refresh(claims: Annotated[Claims, Depends(JWT.get_claims())]) -> Token:
    token = await login_service.refresh(claims)
    return token


@router.get(
    "/verify",
    summary="토큰 유효성 확인",
    description="- 발행된 토큰이 사용가능한지 확인합니다.(아직 로그인되어 있는지 확인)",
    dependencies=[Depends(JWT.verify)],
    responses=Status.docs(ER.INVALID_TOKEN, ER.UNAUTHORIZED),
)
async def verify():
    return SU.SUCCESS
