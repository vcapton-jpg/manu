"""FastAPI app + lifespan."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from polymarket_advisor.api.router import api_router
from polymarket_advisor.db import init_engine
from polymarket_advisor.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    init_engine()
    yield
    # teardown if needed


app = FastAPI(title="Polymarket Advisor API", lifespan=lifespan)
app.include_router(api_router)
