"""
Railway 12306 Main Application
FastAPI main entry point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from jose import JWTError
from loguru import logger

from app.core.config import settings
from app.api.v1.router import api_router
from app.db.init_db import init_db
from app.core.middleware import SecurityMiddleware, RateLimitMiddleware, RequestValidationMiddleware
from app.core.exceptions import (
    BusinessException,
    http_exception_handler,
    starlette_http_exception_handler,
    validation_exception_handler,
    business_exception_handler,
    sqlalchemy_exception_handler,
    jwt_exception_handler,
    general_exception_handler
)

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

# Add security middleware
app.add_middleware(SecurityMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)
app.add_middleware(RequestValidationMiddleware)

# Add exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(StarletteHTTPException, starlette_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(JWTError, jwt_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


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

