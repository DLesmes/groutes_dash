"""
Data models for visit records and location data
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
import re

class Location(BaseModel):
    """Model for location coordinates"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    
    @classmethod
    def from_string(cls, point_string: str) -> "Location":
        """
        Create Location from string with coordinates separated by space
        
        Args:
            point_string: String with coordinates like "19.4326 -99.1332"
            
        Returns:
            Location object with parsed coordinates
        """
        try:
            # Split by space and convert to float
            coords = point_string.strip().split()
            if len(coords) != 2:
                raise ValueError(f"Expected 2 coordinates, got {len(coords)}")
            
            lat, lon = float(coords[0]), float(coords[1])
            
            # Validate coordinates
            if not (-90 <= lat <= 90):
                raise ValueError(f"Latitude must be between -90 and 90, got {lat}")
            if not (-180 <= lon <= 180):
                raise ValueError(f"Longitude must be between -180 and 180, got {lon}")
            
            return cls(latitude=lat, longitude=lon)
            
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid coordinate format: {point_string}. Error: {e}")

class VisitRecord(BaseModel):
    """Model for a single visit record from CSV"""
    timestamp: datetime = Field(..., description="Timestamp of the visit")
    point: str = Field(..., description="Coordinates as string")
    place: str = Field(..., description="Place name or description")
    
    # Computed fields
    location: Optional[Location] = None
    
    @validator('location', pre=True, always=True)
    def parse_location(cls, v, values):
        """Parse location from point string"""
        if 'point' in values:
            try:
                return Location.from_string(values['point'])
            except ValueError as e:
                # Log error but don't fail validation
                print(f"Warning: Could not parse location from '{values['point']}': {e}")
                return None
        return v
    
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