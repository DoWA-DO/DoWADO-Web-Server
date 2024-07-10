from fastapi import APIRouter, Depends, HTTPException
from src.core.status import Status, SU, ER
from src.api.v1.login.login_control import get_current_user
from src.api.v1.chatbot.chatbot_dto import ChatCreateRequest
from src.api.v1.chatbot.chatbot_service import ChatService
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chatbot", tags=["채팅 NEW"])

@router.post(
    "/",
    summary="채팅 메시지 전송",
    description="- 로그인된 사용자의 이름과 채팅 메시지를 Chat DB의 chat 테이블에 저장",
    response_model=ChatCreateRequest,
    responses=Status.docs(SU.SUCCESS, ER.DUPLICATE_RECORD)
)
async def create_chat(
    chat_request: ChatCreateRequest,
    current_user: str = Depends(get_current_user),
    chat_service: ChatService = Depends(ChatService)
):
    try:
        return await chat_service.create_chat(current_user, chat_request)
    except Exception as e:
        logger.error(f"Error creating chat: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

