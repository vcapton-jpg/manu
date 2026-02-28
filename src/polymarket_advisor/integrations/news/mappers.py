"""Mappers RSS/raw -> domain/db."""
from polymarket_advisor.integrations.news.schemas import NewsItemRaw


def raw_to_news_row(raw: NewsItemRaw) -> dict:
    return {
        "title": raw.get("title", ""),
        "url": raw.get("link") or raw.get("url", ""),
        "published_at": raw.get("published") or raw.get("pubDate"),
        "source": raw.get("source", ""),
        "raw": raw,
    }
