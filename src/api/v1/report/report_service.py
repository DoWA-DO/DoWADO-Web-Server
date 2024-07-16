"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# # 호출할 모듈 추가
from src.api.v1.report.report_dto import KeyReport, CreateReport, ReadReport
from src.api.v1.report import report_dao

# 이후 삭제 예정, 일단 기본 추가
from sqlalchemy.ext.asyncio import AsyncSession


# Read
# async def get_examples(db: AsyncSession) -> list[ReadExampleInfo]:
#     examples_info = await example_dao.get_examples(db)
#     return examples_info

# Create
async def create_report(report: CreateReport, db: AsyncSession) -> None:
    await report_dao.create_example(report, db)

# # Delete
# async def delete_example(example_id: str, db: AsyncSession) -> None:
#     await example_dao.delete_example(example_id, db)