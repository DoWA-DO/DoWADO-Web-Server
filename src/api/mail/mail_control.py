from fastapi import APIRouter
from .mail_dto import EmailRequest
from .mail_service import send_email

router = APIRouter()

@router.post("/send_email")
async def send_email_handler(email_request: EmailRequest):
    return await send_email(email_request)
