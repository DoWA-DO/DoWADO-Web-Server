#router import

from fastapi import APIRouter

from src.api.v1.example.example_control import router as example_router
from src.api.v1.chat.chat_control import router as chat_router
from src.api.mail.mail_control import router as mail_router
from src.api.v1.super_teacher.super_teacher_control import router as super_teacher_router
from src.api.v1.super_teacher.super_teacher_verify_control import router as super_teacher_verify_router

router = APIRouter()
router.include_router(example_router)
router.include_router(chat_router)
router.include_router(super_teacher_router)
router.include_router(super_teacher_verify_router)