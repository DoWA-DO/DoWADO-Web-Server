# chatbot_control.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from src.core.status import Status, SU, ER
from src.api.v1.login.login_control import get_current_user
from src.api.v1.chat.chatbot_dto import ChatCreateRequest, ChatCreateResponse
from src.api.v1.chat.chatbot_service import ChatService
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chatbot", tags=["채팅"])

# Upload
@router.post(
    "/upload",
    summary="채팅 메시지 전송",
    description="- 로그인된 사용자의 이름과 채팅 메시지를 Chat DB의 chat 테이블에 저장",
    response_model=ChatCreateRequest, 
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
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

# Read
@router.get(
    "/read",
    summary="채팅 내역 조회",
    description="- 모든 사용자의 채팅 내역 조회, 없으면 [] 출력",
    response_model=List[ChatCreateResponse],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)

async def read_chat(
    current_user: str = Depends(get_current_user),
    chat_service: ChatService = Depends(ChatService)
): 
    chats = await chat_service.read_chat(current_user)
    return [
        ChatCreateResponse(
        id=chat.id,
        chat_content=chat.chat_content,
        chat_student_email=chat.chat_student_email,
        chat_date=chat.chat_date,
        chat_status=chat.chat_status 
    ) for chat in chats
    ]
    
# Delete
@router.delete(
    "/delete",
    summary="채팅 내역 삭제",
    description="- 현재 로그인된 사용자의 채팅 내역 전부 삭제",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST)
)
async def delete_chat(
    current_user: str = Depends(get_current_user),
    chat_service: ChatService = Depends(ChatService)
):
    try:
        await chat_service.delete_chat(current_user)
        return {"detail": "Chats deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting chats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    