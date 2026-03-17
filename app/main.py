"""
FastAPI application entry point.
"""

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes_generate import router as generate_router
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Create the FastAPI app
app = FastAPI(
    title="AI-Powered Manim Animator",
    description="Generate educational math animation videos using AI and Manim",
    version="1.0.0",
)

# CORS — allow everything for debugging connection issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the videos directory exists and mount it as static files
videos_dir = Path(settings.VIDEO_OUTPUT_DIR)
videos_dir.mkdir(parents=True, exist_ok=True)
app.mount("/videos", StaticFiles(directory=str(videos_dir)), name="videos")

# Include API routes
app.include_router(generate_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "app": "AI-Powered Manim Animator",
        "docs": "/docs",
        "health": "/health",
    }
