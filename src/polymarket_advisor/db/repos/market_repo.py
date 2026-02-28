"""Market repository."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from polymarket_advisor.db.models import Market


class MarketRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_slug(self, slug: str) -> Market | None:
        r = await self.session.execute(select(Market).where(Market.slug == slug))
        return r.scalar_one_or_none()

    async def upsert(self, slug: str, question: str | None = None, end_date_iso: str | None = None, raw: dict | None = None) -> Market:
        m = await self.get_by_slug(slug)
        if m:
            if question is not None:
                m.question = question
            if end_date_iso is not None:
                m.end_date_iso = end_date_iso
            if raw is not None:
                m.raw = raw
            return m
        m = Market(slug=slug, question=question, end_date_iso=end_date_iso, raw=raw)
        self.session.add(m)
        await self.session.flush()
        return m
