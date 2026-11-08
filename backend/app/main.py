from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.database.connection import engine, check_database_connection
from app.database.base import Base
import app.models  # Ensures all ORM models are registered with Base metadata
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    setup_logging()
    logger.info("Initializing %s Backend Services...", settings.PROJECT_NAME)
    is_healthy, msg = check_database_connection()
    if is_healthy:
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database schemas verified/created.")
        except Exception as e:
            logger.warning("Database schema verification failed: %s", e)
    else:
        logger.warning("Database not connected during startup (%s); schema migration skipped.", msg)
    yield
    # Shutdown actions
    logger.info("Shutting down %s Backend Services.", settings.PROJECT_NAME)


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Explainable AI Decision-Support Platform for Pharmaceutical Stockout Risk, Expiry Prevention, and Inventory Redistribution in Ethiopian Healthcare Facilities.",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# Set up CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API v1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"], summary="Liveness check")
def liveness_check():
    """Quick liveness probe for orchestrators and load balancers."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get(f"{settings.API_V1_STR}/health", tags=["Health"], summary="Comprehensive readiness check")
def readiness_check():
    """Readiness probe that checks database connectivity and core services."""
    db_healthy, db_message = check_database_connection()
    db_type = "sqlite" if settings.DATABASE_URL.startswith("sqlite") else "postgresql"

    payload = {
        "status": "healthy" if db_healthy else "degraded",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": {
            "status": "connected" if db_healthy else "disconnected",
            "type": db_type,
            "message": db_message,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if not db_healthy:
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=payload)
    return payload


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
