# chat_control.py

import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1.chat.chatbot_dto import ChatCreateResponse
from src.api.v1.login.login_control import get_current_user
from src.core.status import Status, SU, ER
from src.database.session import get_db


from .intoGPT import create_prediction_prompt

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chatbot", tags=["채팅"])

class RequestResumeScript(BaseModel):
    content: str
    
@router.post(
    "/chat",
    summary="진로 상담 챗봇에게 채팅 메시지 전송",
    description="- 채팅 메시지를 기입 후 전송하면, 챗봇의 답장이 반환됨.",
    response_model = ChatCreateResponse,
    responses = Status.docs(SU.ACCEPTED, ER.FIELD_VALIDATION_ERROR)
)
async def create_prediction_question(data: RequestResumeScript):
    try:
        print(data.content)
        content = create_prediction_prompt(data.content)
        if content is None:
            raise HTTPException(status_code=204, detail="Something went wrong")
        response_data = {
            "data": content
        }
    except HTTPException as e:
        response_data = {
            "status": e.status_code,
            "data": "죄송합니다. 오류로 인해 예상 질문이 생성되지 않았습니다. 다시 시도해주세요."
        }
    return JSONResponse(content=response_data)

async def create_chatbot_message(
    query: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    username = current_user.get('username')
    response = await create_chatbot_message(query, username, db)
    return response

