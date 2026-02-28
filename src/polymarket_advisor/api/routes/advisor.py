"""GET /advisor."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from polymarket_advisor.api.deps import get_db_session
from polymarket_advisor.services.advisor import get_advisor_recommendation
from polymarket_advisor.api.schemas.advisor import AdvisorOut

router = APIRouter()


@router.get("", response_model=AdvisorOut)
async def get_advisor(
    profile: str = "medium",
    risk: str = "medium",
    horizon: str = "short",
    session: AsyncSession = Depends(get_db_session),
) -> AdvisorOut:
    data = await get_advisor_recommendation(session, profile=profile, risk=risk, horizon=horizon)
    return AdvisorOut(
        thesis=data.get("thesis", ""),
        signals=data.get("signals", []),
        risk_notes=data.get("risk_notes"),
        catalysts=data.get("catalysts", []),
        sizing=data.get("sizing"),
    )
