"""Pydantic models for API request/response schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PersonCreate(BaseModel):
    """Schema for registering a new person."""
    name: str = Field(..., min_length=1, max_length=100)
    metadata: Optional[dict] = Field(default_factory=dict)


class PersonResponse(BaseModel):
    """Schema for person response."""
    id: str
    name: str
    metadata: dict
    face_count: int
    created_at: datetime
    updated_at: datetime


class RecognitionResult(BaseModel):
    """Schema for face recognition result."""
    matched: bool
    person_id: Optional[str] = None
    name: Optional[str] = None
    confidence: Optional[float] = None
    metadata: Optional[dict] = None
    message: str


class HealthResponse(BaseModel):
    """Schema for health check."""
    status: str = "healthy"
    mongodb_connected: bool
