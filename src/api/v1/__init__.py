#router import

from fastapi import APIRouter

from src.api.v1.example.example_control import router as example_router
from src.api.v1.chat.chat_control import router as chat_router

router = APIRouter()
router.include_router(example_router)
router.include_router(chat_router)