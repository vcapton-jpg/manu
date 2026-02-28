"""RSS -> upsert news_items."""
from sqlalchemy.ext.asyncio import AsyncSession
from polymarket_advisor.integrations.news import RssClient
from polymarket_advisor.integrations.news.mappers import raw_to_news_row
from polymarket_advisor.db.repos import NewsRepo


async def refresh_news(session: AsyncSession, feed_url: str) -> int:
    client = RssClient(feed_url)
    items = await client.fetch()
    repo = NewsRepo(session)
    count = 0
    for raw in items:
        row = raw_to_news_row(raw)
        await repo.upsert_by_url(
            url=row.get("url", ""),
            title=row.get("title"),
            source=row.get("source"),
            published_at=row.get("published_at"),
            raw=row.get("raw"),
        )
        count += 1
    return count
