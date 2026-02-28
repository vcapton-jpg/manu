"""Price repository."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from polymarket_advisor.db.models import Price
from datetime import datetime


class PriceRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def insert(self, token_id: int, price: float, ts: datetime) -> Price:
        p = Price(token_id=token_id, price=price, ts=ts)
        self.session.add(p)
        await self.session.flush()
        return p
