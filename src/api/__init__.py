from fastapi import APIRouter

from src.api.chat.chat_control import router as chat_router

router = APIRouter()
router.include_router(chat_router)