from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import logging

from app.routers import auth, investigations, tools, health, reports, integration
from app.database import engine, Base, get_db
from app.core.rate_limit import RateLimitMiddleware

# Create tables
Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="OSINT Platform 2026",
    description="Hybrid OSINT platform with 50+ integrated tools",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting middleware
app.add_middleware(RateLimitMiddleware)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(investigations.router, prefix="/investigations", tags=["investigations"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(integration.router, prefix="/integration", tags=["integration"])
app.include_router(tools.router, prefix="/tools", tags=["tools"])

@app.get("/")
async def root():
    return {
        "message": "OSINT Platform 2026",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "auth": "/auth",
            "investigations": "/investigations",
            "tools": "/tools"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
