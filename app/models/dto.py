"""
Pydantic DTOs for API request/response models.
"""

from pydantic import BaseModel, Field
from typing import Optional


class GenerateRequest(BaseModel):
    """Request body for POST /api/generate_video."""
    concept: str = Field(..., min_length=1, max_length=300, description="Math concept to animate")
    language: str = Field(default="English", description="Language for on-screen text")


class GenerateResponse(BaseModel):
    """Response body for POST /api/generate_video."""
    status: str = Field(..., description="'success' or 'error'")
    video_url: Optional[str] = Field(default=None, description="URL to the rendered MP4")
    message: Optional[str] = Field(default=None, description="User-friendly message")
    details: Optional[str] = Field(default=None, description="Technical details (errors)")
