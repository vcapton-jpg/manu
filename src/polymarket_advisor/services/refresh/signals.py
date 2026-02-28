"""Create signal_run + insert signals (single snapshot timestamp)."""
from sqlalchemy.ext.asyncio import AsyncSession

from polymarket_advisor.core.time import utc_now
from polymarket_advisor.db.repos import SignalRepo
from polymarket_advisor.domain.scoring import compute_score, compute_confidence


async def refresh_signals(session: AsyncSession, token_scores: list[dict]) -> int:
    """
    token_scores: list of dicts, each like:
      { token_id: int, edge?: float, confidence?: float, score?: float }
    """
    repo = SignalRepo(session)

    # One run = one snapshot timestamp
    run = await repo.create_run(run_ts=utc_now())

    count = 0
    for item in token_scores:
        token_id = item.get("token_id")
        if token_id is None:
            continue

        edge = float(item.get("edge", 0.0))
        confidence = item.get("confidence")
        confidence = float(confidence) if confidence is not None else float(compute_confidence())

        score = item.get("score")
        score = float(score) if score is not None else float(compute_score(edge, confidence))

        await repo.insert_signal(
            signal_run_id=run.id,
            token_id=int(token_id),
            score=score,
            edge=edge,
            confidence=confidence,
            ts=run.run_ts,  # ✅ same ts for the whole snapshot
        )
        count += 1

    return count