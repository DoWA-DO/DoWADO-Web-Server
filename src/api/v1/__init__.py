from fastapi import APIRouter

from src.api.v1.example.example_control import router as example_router

router = APIRouter()
router.include_router(example_router)