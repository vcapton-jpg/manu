"""Momentum / features simples."""
from typing import Any


def compute_momentum(prices: list[float] | list[dict[str, Any]]) -> float:
    """Placeholder: calcul momentum à partir de séries de prix."""
    if not prices:
        return 0.0
    if isinstance(prices[0], dict):
        prices = [p.get("price", 0) for p in prices if p.get("price") is not None]
    if len(prices) < 2:
        return 0.0
    return float(prices[-1] or 0) - float(prices[0] or 0)
