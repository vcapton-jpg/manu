"""Advisor recommendation repository."""
from datetime import datetime
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from polymarket_advisor.db.models import AdvisorReco


class AdvisorRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_latest(self, profile: str | None = None) -> AdvisorReco | None:
        q = select(AdvisorReco)
        if profile:
            q = q.where(AdvisorReco.profile == profile)
        q = q.order_by(desc(AdvisorReco.run_ts)).limit(1)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    async def insert(self, run_ts: datetime, profile: str | None, payload: dict, thesis: str | None = None, risk_notes: str | None = None) -> AdvisorReco:
        rec = AdvisorReco(run_ts=run_ts, profile=profile, payload=payload, thesis=thesis, risk_notes=risk_notes)
        self.session.add(rec)
        await self.session.flush()
        return rec
