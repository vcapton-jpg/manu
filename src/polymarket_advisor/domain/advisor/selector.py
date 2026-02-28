"""Sélection top signals par score."""
from typing import Any


def select_top_signals(signals: list[dict[str, Any]], min_score: float = 0.3, max_n: int = 10) -> list[dict[str, Any]]:
    """Filtre et trie par score décroissant."""
    filtered = [s for s in signals if (s.get("score") or 0) >= min_score]
    sorted_s = sorted(filtered, key=lambda x: -(x.get("score") or 0))
    return sorted_s[:max_n]
