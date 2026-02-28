"""Include all route modules."""
from fastapi import APIRouter
from polymarket_advisor.api.routes.health import router as health_router
from polymarket_advisor.api.routes.signals import router as signals_router
from polymarket_advisor.api.routes.refresh import router as refresh_router
from polymarket_advisor.api.routes.news import router as news_router
from polymarket_advisor.api.routes.advisor import router as advisor_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(signals_router, prefix="/signals", tags=["signals"])
api_router.include_router(refresh_router, prefix="/refresh", tags=["refresh"])
api_router.include_router(news_router, prefix="/news", tags=["news"])
api_router.include_router(advisor_router, prefix="/advisor", tags=["advisor"])
