"""Confidence scoring."""
from typing import Any


def compute_confidence(volume: float = 0, liquidity: float = 0, n_samples: int = 0) -> float:
    """Placeholder: confidence entre 0 et 1."""
    if n_samples:
        return min(1.0, 0.3 + 0.7 * (min(n_samples, 100) / 100))
    if volume or liquidity:
        return min(1.0, 0.2 + 0.8 * min((volume + liquidity) / 10000, 1.0))
    return 0.5
