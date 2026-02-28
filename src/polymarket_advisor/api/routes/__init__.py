# Routes are mounted from api/router.py
from polymarket_advisor.api.routes import health, refresh, signals, news, advisor

__all__ = ["health", "refresh", "signals", "news", "advisor"]
