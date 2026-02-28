"""GET /signals — latest signals."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from polymarket_advisor.api.deps import get_db_session
from polymarket_advisor.db.repos import SignalRepo
from polymarket_advisor.api.schemas.signals import SignalOut, SignalListResponse

router = APIRouter()


@router.get("", response_model=SignalListResponse)
async def get_signals(session: AsyncSession = Depends(get_db_session)) -> SignalListResponse:
    repo = SignalRepo(session)
    run_id = await repo.get_latest_run_id()
    if not run_id:
        return SignalListResponse(signals=[], run_id=None)
    signals_orm = await repo.get_signals_for_run(run_id)
    signals = [
        SignalOut(
            token_id=s.token_id,
            score=float(s.score) if s.score is not None else None,
            edge=float(s.edge) if s.edge is not None else None,
            confidence=float(s.confidence) if s.confidence is not None else None,
            ts=s.ts,
        )
        for s in signals_orm
    ]
    return SignalListResponse(signals=signals, run_id=run_id)
