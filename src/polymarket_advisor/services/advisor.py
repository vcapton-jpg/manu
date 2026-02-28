"""Product service: domain + repos pour advisor."""
from sqlalchemy.ext.asyncio import AsyncSession
from polymarket_advisor.db.repos import SignalRepo, AdvisorRepo
from polymarket_advisor.domain.advisor import get_thresholds, select_top_signals, compose_thesis
from polymarket_advisor.core.time import utc_now


async def get_advisor_recommendation(session: AsyncSession, profile: str = "medium", risk: str = "medium", horizon: str = "short") -> dict:
    signal_repo = SignalRepo(session)
    advisor_repo = AdvisorRepo(session)
    run_id = await signal_repo.get_latest_run_id()
    if not run_id:
        return {"thesis": "No signals yet.", "signals": [], "risk_notes": "N/A"}
    signals_orm = await signal_repo.get_signals_for_run(run_id)
    signals = [
        {
            "token_id": s.token_id,
            "score": float(s.score) if s.score is not None else None,
            "edge": float(s.edge) if s.edge is not None else None,
            "confidence": float(s.confidence) if s.confidence is not None else None,
        }
        for s in signals_orm
    ]
    thresholds = get_thresholds(risk=risk, horizon=horizon)
    selected = select_top_signals(
        signals,
        min_score=thresholds.get("min_score", 0.3),
        max_n=thresholds.get("max_signals", 10),
    )
    composed = compose_thesis(selected)
    # Optionally persist
    await advisor_repo.insert(
        run_ts=utc_now(),
        profile=profile,
        payload=composed,
        thesis=composed.get("thesis"),
        risk_notes=composed.get("risk_notes"),
    )
    return composed
