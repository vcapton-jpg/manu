"""POST /refresh/signals, etc."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from polymarket_advisor.api.deps import get_db_session
from polymarket_advisor.services.refresh import refresh_markets, refresh_prices, refresh_signals, refresh_news

router = APIRouter()


@router.post("/signals")
async def refresh_signals_endpoint(session: AsyncSession = Depends(get_db_session)) -> dict:
    # Option: accept body with token_scores; for now empty = no new signals
    count = await refresh_signals(session, [])
    return {"status": "ok", "signals_created": count}


@router.post("/markets")
async def refresh_markets_endpoint(session: AsyncSession = Depends(get_db_session)) -> dict:
    count = await refresh_markets(session)
    return {"status": "ok", "markets_updated": count}


@router.post("/news")
async def refresh_news_endpoint(session: AsyncSession = Depends(get_db_session), feed_url: str = "") -> dict:
    if not feed_url:
        return {"status": "skipped", "message": "feed_url required"}
    count = await refresh_news(session, feed_url)
    return {"status": "ok", "news_updated": count}
