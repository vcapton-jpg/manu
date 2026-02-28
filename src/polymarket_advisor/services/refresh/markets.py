"""Gamma -> upsert markets/tokens."""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from polymarket_advisor.integrations.polymarket import GammaClient
from polymarket_advisor.integrations.polymarket.mappers import (
    event_to_market_row,
    token_from_market,
    token_identifiers,
)
from polymarket_advisor.db.repos import MarketRepo, TokenRepo


async def refresh_markets(session: AsyncSession, limit: int = 100) -> int:
    client = GammaClient()
    events = await client.get_events(limit=limit)

    market_repo = MarketRepo(session)
    token_repo = TokenRepo(session)

    inserted_or_updated = 0

    for ev in events:
        row = event_to_market_row(ev)
        slug = row.get("slug")
        if not slug:
            continue

        market = await market_repo.upsert(
            slug=slug,
            question=row.get("question"),
            end_date_iso=row.get("end_date_iso"),
            raw=row.get("raw"),
        )
        inserted_or_updated += 1

        # Fetch markets under this event and ingest tokens
        markets = await client.get_markets(event_slug=slug)
        for m in markets:
            tokens = token_from_market(m)
            for t in tokens:
                ids = token_identifiers(t)
                await token_repo.upsert(
                    market_id=market.id,
                    outcome=t.get("name") or t.get("outcome") or t.get("label"),
                    token_id=ids.get("token_id"),
                    raw=t,
                )
                inserted_or_updated += 1

    return inserted_or_updated