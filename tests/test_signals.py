"""Tests signals (domain + repo logic if needed)."""
import pytest
from polymarket_advisor.domain.scoring import compute_score, compute_confidence, compute_momentum


def test_compute_confidence() -> None:
    assert 0 <= compute_confidence(n_samples=50) <= 1
    assert compute_confidence(n_samples=0) == 0.5


def test_compute_score() -> None:
    assert compute_score(0.1, 0.8) == pytest.approx(0.08)
    assert compute_score(-0.2, 0.5) == 0.1


def test_compute_momentum() -> None:
    assert compute_momentum([1.0, 2.0]) == 1.0
    assert compute_momentum([]) == 0.0
