"""Token repository."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from polymarket_advisor.db.models import Token


class TokenRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def upsert(
        self,
        market_id: int,
        outcome: str | None,
        token_id: str | None,
        raw: dict | None,
    ) -> Token:
        """
        Upsert token for a given market.
        We consider (market_id, outcome) as identity for now.
        If outcome is missing, we fall back to (market_id, token_id) when available.
        """
        q = select(Token).where(Token.market_id == market_id)

        if outcome:
            q = q.where(Token.outcome == outcome)
        elif token_id:
            q = q.where(Token.token_id == token_id)
        else:
            # No stable identity -> insert new
            tok = Token(market_id=market_id, outcome=outcome, token_id=token_id, raw=raw)
            self.session.add(tok)
            await self.session.flush()
            return tok

        r = await self.session.execute(q.limit(1))
        tok = r.scalar_one_or_none()

        if tok is None:
            tok = Token(market_id=market_id, outcome=outcome, token_id=token_id, raw=raw)
            self.session.add(tok)
            await self.session.flush()
            return tok

        # update
        tok.outcome = outcome or tok.outcome
        tok.token_id = token_id or tok.token_id
        tok.raw = raw or tok.raw
        await self.session.flush()
        return tok