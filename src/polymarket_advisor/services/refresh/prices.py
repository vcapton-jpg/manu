"""CLOB/Gamma -> insert prices."""
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from polymarket_advisor.core.time import utc_now
from polymarket_advisor.db.repos import PriceRepo


async def refresh_prices(session: AsyncSession, token_id: int, price: float, ts: datetime | None = None) -> int:
    repo = PriceRepo(session)
    await repo.insert(token_id=token_id, price=price, ts=ts or utc_now())
    return 1
