"""
메인 서버 모듈
"""
from src.core import DowaDOAPI
from src.core import cors, error, event, router
import logging


logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

app = DowaDOAPI(**{
    "title" : "Do:WADO API Server",
    "description" : "Do:WADO 청소년 AI 진로 추천 서비스",
    "version" : "0.1",
    "docs_url" : "/docs",
    "redoc_url" : "/redoc",
})

# 확장 모듈 등록
app.use(cors)
app.use(error)
app.use(router, base="./src/api")
app.use(event)

_logger.info('=>> 서버 시작 중...')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)