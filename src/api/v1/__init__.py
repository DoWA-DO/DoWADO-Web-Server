from fastapi import APIRouter

from src.api.v1.example.example_control import router as example_router
from src.api.v1.teacher.teacher_control import router as teacher_router

router = APIRouter()
router.include_router(example_router)
router.include_router(teacher_router)