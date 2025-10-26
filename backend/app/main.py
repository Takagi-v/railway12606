"""
Railway 12306 Main Application
FastAPI main entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings
from app.api.v1.router import api_router
from app.db.init_db import init_db

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Railway 12306 Train Ticket Booking System",
    version="1.0.0",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
    openapi_url=f"{settings.API_PREFIX}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Starting Railway 12306 API Server...")
    # Initialize database tables
    # Uncomment the following line after setting up database
    # init_db()


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Shutting down Railway 12306 API Server...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Railway 12306 API",
        "docs": f"{settings.API_PREFIX}/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Include API router
app.include_router(api_router, prefix=settings.API_PREFIX)

