"""GET /news."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from polymarket_advisor.api.deps import get_db_session
from polymarket_advisor.db.repos import NewsRepo
from polymarket_advisor.api.schemas.news import NewsOut, NewsListResponse

router = APIRouter()


@router.get("", response_model=NewsListResponse)
async def get_news(limit: int = 50, session: AsyncSession = Depends(get_db_session)) -> NewsListResponse:
    repo = NewsRepo(session)
    items = await repo.list_recent(limit=limit)
    return NewsListResponse(news=[NewsOut.model_validate(i) for i in items])
