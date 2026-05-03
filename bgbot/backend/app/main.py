import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from shared.config import settings
from shared.logging import setup_logging
from app.core.database import init_db
from app.middleware.security import SecurityHeadersMiddleware
from app.middleware.rate_limit import RateLimitMiddleware

import app.models  # noqa: F401

setup_logging("backend")
logger = logging.getLogger("bgbot")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 50)
    logger.info("BG-BOT v5 API Starting")
    await init_db()
    logger.info("Database connected")
    logger.info("=" * 50)
    yield
    try:
        from app.core.redis import redis_client
        await redis_client.close()
    except Exception:
        pass
    try:
        from app.core.database import engine
        await engine.dispose()
    except Exception:
        pass
    logger.info("BG-BOT v5 API shut down")


app = FastAPI(title="BG-BOT v5", version="5.0.0", lifespan=lifespan)

# Middleware
try:
    from app.middleware.metrics import MetricsMiddleware
    app.add_middleware(MetricsMiddleware)
except ImportError:
    logger.warning("MetricsMiddleware not found, skipping")

app.add_middleware(RateLimitMiddleware, max_req=settings.MAX_REQUESTS_PER_MINUTE)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus
try:
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
except Exception:
    pass

# Routes
from app.routes.auth import router as auth_router
from app.routes.trades import router as trades_router
from app.routes.bot import router as bot_router
from app.routes.backtest import router as backtest_router
from app.routes.websocket import router as ws_router

app.include_router(auth_router)
app.include_router(trades_router)
app.include_router(bot_router)
app.include_router(backtest_router)
app.include_router(ws_router)

# Optional routes
try:
    from app.routes.oauth import router as oauth_router
    app.include_router(oauth_router)
except ImportError:
    pass

try:
    from app.routes.security import router as security_router
    app.include_router(security_router)
except ImportError:
    pass


@app.get("/health")
async def health():
    checks = {"status": "ok", "version": "5.0.0"}
    try:
        from app.core.redis import redis_client
        await redis_client.ping()
        checks["redis"] = "ok"
    except Exception:
        checks["redis"] = "error"
        checks["status"] = "degraded"
    try:
        from app.core.database import engine
        import sqlalchemy
        async with engine.connect() as conn:
            await conn.execute(sqlalchemy.text("SELECT 1"))
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "error"
        checks["status"] = "degraded"
    return checks
