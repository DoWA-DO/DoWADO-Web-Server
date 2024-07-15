from fastapi import APIRouter
from .mail_dto import EmailRequest
from .mail_service import generate_verification_code, send_email
import logging


# 로깅 및 라우터 객체 생성 - 기본적으로 추가
logger = logging.getLogger(__name__)
router = APIRouter(tags=["naver smtp"])

@router.post("/send_email")
async def send_email_handler(email_request: EmailRequest):
    verification_code = generate_verification_code()
    response = await send_email(email_request, verification_code)
    return {"verification_code": verification_code, "message": response["message"]}
