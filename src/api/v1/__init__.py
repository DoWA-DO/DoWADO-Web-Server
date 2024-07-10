#router import

from fastapi import APIRouter

from src.api.v1.super_teacher.super_teacher_control import router as super_teacher_router
from src.api.v1.login.login_control import router as login_router
from src.api.v1.chatbot.chatbot_control import router as chatbot_router

router = APIRouter()
router.include_router(super_teacher_router)
router.include_router(login_router)
router.include_router(chatbot_router)