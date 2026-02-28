"""Risk/horizon -> thresholds."""
from typing import Any


def get_thresholds(risk: str = "medium", horizon: str = "short") -> dict[str, Any]:
    """Seuils min score / confidence selon profil."""
    return {
        "min_score": 0.3,
        "min_confidence": 0.4,
        "max_signals": 10,
    }
