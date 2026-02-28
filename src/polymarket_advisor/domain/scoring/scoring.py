"""Score = f(edge, confidence)."""
from polymarket_advisor.domain.scoring.confidence import compute_confidence


def compute_score(edge: float, confidence: float | None = None, **kwargs: object) -> float:
    """Score = abs(edge) * confidence."""
    if confidence is None:
        confidence = compute_confidence(**kwargs)
    return abs(edge) * confidence
