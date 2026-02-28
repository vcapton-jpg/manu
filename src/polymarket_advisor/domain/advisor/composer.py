"""Thesis / catalysts / risk_notes / sizing."""
from typing import Any


def compose_thesis(signals: list[dict[str, Any]], risk_notes: str | None = None) -> dict[str, Any]:
    """Compose payload advisor (thesis, catalysts, risk_notes, sizing)."""
    return {
        "thesis": "Top signals by edge and confidence.",
        "catalysts": [],
        "risk_notes": risk_notes or "Standard risk.",
        "sizing": "Equal weight among selected.",
        "signals": signals,
    }
