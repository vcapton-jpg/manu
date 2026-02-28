"""News repository."""
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from polymarket_advisor.db.models import NewsItem


class NewsRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_recent(self, limit: int = 50) -> list[NewsItem]:
        r = await self.session.execute(
            select(NewsItem).order_by(desc(NewsItem.published_at)).limit(limit)
        )
        return list(r.scalars().all())

    async def upsert_by_url(self, url: str, title: str | None = None, source: str | None = None, published_at=None, raw: dict | None = None) -> NewsItem:
        r = await self.session.execute(select(NewsItem).where(NewsItem.url == url))
        existing = r.scalar_one_or_none()
        if existing:
            if title is not None:
                existing.title = title
            if source is not None:
                existing.source = source
            if published_at is not None:
                existing.published_at = published_at
            if raw is not None:
                existing.raw = raw
            return existing
        n = NewsItem(url=url, title=title, source=source, published_at=published_at, raw=raw)
        self.session.add(n)
        await self.session.flush()
        return n
