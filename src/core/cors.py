# cors.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi.exceptions import HTTPException
from src.config.security import JWT


class ClaimsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if token:
            token = token.split(" ")[1]  # "Bearer <token>" 형식에서 토큰만 추출
            try:
                JWT.verify(request, token)
            except HTTPException as e:
                return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        response = await call_next(request)
        return response


def use(app: FastAPI):
    """ FastAPI 애플리케이션에 CORS 및 Claims 미들웨어 확장 모듈 """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],     # 모든 도메인 요청 허용
        allow_methods=["*"],     # 모든 메서드 요청 허용
        allow_headers=["*"],     # 요청 시 모든 헤더 허용
        expose_headers=["*"],    # 모든 헤더 자바스크립트 접근 허용
        allow_credentials=True,  # 쿠키, 인증 헤더 요청 허용
    )
    app.add_middleware(ClaimsMiddleware)
