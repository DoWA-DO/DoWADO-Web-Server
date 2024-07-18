#router import

from fastapi import APIRouter

from src.api.v1.users.teacher.teacher_control import router as teacher_router
from src.api.v1.users.student.student_control import router as student_router
from src.api.v1.login.login_control import router as login_router
from src.api.v1.mail.mail_control import router as mail_router
from src.api.v1.chatbot.chat_control import router as chatbot_router
from src.api.v1.file.file_control import router as file_router

router = APIRouter()
router.include_router(teacher_router)
router.include_router(student_router)
router.include_router(login_router)
router.include_router(chatbot_router)
router.include_router(mail_router)
router.include_router(file_router)