"""
레포트 생성
"""
from typing import Annotated
from typing import Optional
from fastapi import APIRouter, Depends, Request
from src.config.status import Status, SU, ER
from src.api.report import report_service
from src.config.security import JWT, Claims
import logging


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/report", tags=["진로 추천 레포트 관련 API"])


@router.post(
    "/predict",
    summary     = "채팅 로그 저장 및 진로 추천",
    description = "- 채팅 로그를 저장하고 해당 로그를 기반으로 모델 추론을 통해 진로 추천 + 레포트 생성",
    dependencies=[Depends(JWT.verify)],
    responses   = Status.docs(SU.SUCCESS, ER.INVALID_TOKEN)
)
async def save_chatlog_and_get_recommendation(
    user_id: Annotated[str, Depends(JWT.get_claims("user_id"))],
    session_id: str,
):
    recommendation = await report_service.save_chatlog_and_get_recommendation(session_id, user_id)
    return recommendation
