from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.api.v1.super_teacher.super_teacher_dto import VerifyTeacherEmail
from src.api.v1.super_teacher import super_teacher_service
from src.core.status import Status, SU, ER
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/teacher", tags=["teacher"])

# Verify
@router.post(
    "/verify",
    summary="메일 인증",
    description="메일 인증 여부 확인",
    responses=Status.docs(SU.SUCCESS, ER.DUPLICATE_RECORD),
)
async def verify_email(
    teacher_email: str,
    db: AsyncSession = Depends(get_db)
    
):
    await super_teacher_service.verify_email(teacher_email, db)
    return SU.SUCCESS