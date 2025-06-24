"""
Data models for visit records and location data
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
import re

class VisitRecord(BaseModel):
    """Model for a single visit record from CSV"""
    timestamp: datetime = Field(..., description="Timestamp of the visit")
    point: str = Field(..., description="Coordinates as string")
    place: str = Field(..., description="Place name or description")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude coordinate")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class VisitResponse(BaseModel):
    """Response model for visit data"""
    success: bool = Field(..., description="Operation success status")
    data: List[VisitRecord] = Field(default_factory=list, description="List of visit records")
    total: int = Field(0, description="Total number of records")
    error: Optional[str] = Field(None, description="Error message if any")