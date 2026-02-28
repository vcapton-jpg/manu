"""Signal repository (signals + signal_runs)."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from polymarket_advisor.db.models import Signal, SignalRun, Token


class SignalRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_run(self, run_ts: datetime) -> SignalRun:
        r = SignalRun(run_ts=run_ts)
        self.session.add(r)
        await self.session.flush()
        return r

    async def get_latest_run_id(self) -> int | None:
        r = await self.session.execute(
            select(SignalRun.id).order_by(desc(SignalRun.run_ts)).limit(1)
        )
        return r.scalar_one_or_none()

    async def get_signals_for_run(
        self,
        run_id: int,
        limit: int = 100,
        min_confidence: float | None = None,
        one_per_market: bool = True,
    ) -> list[Signal]:
        """
        Returns signals for a run, ranked by score desc.
        If one_per_market: returns the best signal per market (window function).
        """
        # Base filter: by run_id
        base_filter = [Signal.signal_run_id == run_id]
        if min_confidence is not None:
            base_filter.append(Signal.confidence >= min_confidence)

        # Sort key: score desc (NULL last implicitly for most DBs, ok for now)
        score_order = desc(Signal.score)

        if not one_per_market:
            q = (
                select(Signal)
                .where(*base_filter)
                .order_by(score_order)
                .limit(limit)
            )
            r = await self.session.execute(q)
            return list(r.scalars().all())

        # one_per_market: rank within each market_id using Token.market_id
        ranked = (
            select(
                Signal,
                func.row_number()
                .over(
                    partition_by=Token.market_id,
                    order_by=score_order,
                )
                .label("rn"),
            )
            .join(Token, Token.id == Signal.token_id)
            .where(*base_filter)
        )

        ranked_subq = ranked.subquery()

        # Map subquery back to Signal ORM
        s_alias = aliased(Signal, ranked_subq)

        q = (
            select(s_alias)
            .where(ranked_subq.c.rn == 1)
            .order_by(desc(ranked_subq.c.score))
            .limit(limit)
        )
        r = await self.session.execute(q)
        return list(r.scalars().all())

    async def insert_signal(
        self,
        signal_run_id: int,
        token_id: int,
        score: float | None = None,
        edge: float | None = None,
        confidence: float | None = None,
        ts: datetime | None = None,
    ) -> Signal:
        """
        Insert one signal row.
        IMPORTANT: always pass ts (should be run.run_ts) to keep snapshot consistent.
        """
        if ts is None:
            raise ValueError("ts must be provided (use SignalRun.run_ts)")

        s = Signal(
            signal_run_id=signal_run_id,
            token_id=token_id,
            score=score,
            edge=edge,
            confidence=confidence,
            ts=ts,
        )
        self.session.add(s)
        await self.session.flush()
        return s
