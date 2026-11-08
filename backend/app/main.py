from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.database.connection import engine
from app.database.base import Base
import app.models  # Ensures all ORM models are registered with Base metadata
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    setup_logging()
    logger.info("Initializing PharmaIntelligence AI Backend Services...")
    try:
        # Create database tables if they do not exist
        Base.metadata.create_all(bind=engine)
        logger.info("Database schemas verified/created.")
    except Exception as e:
        logger.warning(f"Database connection deferred or failed during startup: {e}")
    yield
    # Shutdown actions
    logger.info("Shutting down PharmaIntelligence AI Backend Services.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Explainable AI Decision-Support Platform for Pharmaceutical Stockout Risk, Expiry Prevention, and Inventory Redistribution in Ethiopian Healthcare Facilities.",
    version="0.1.0",
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


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "api_v1_docs": f"{settings.API_V1_STR}/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
