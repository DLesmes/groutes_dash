from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import pandas as pd
from pathlib import Path
import logging
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Import from the new structure
from models.visits import VisitRecord, VisitResponse
from utils.csv_utils import load_visits_from_csv
from settings import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=settings.log_file
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="API for managing and analyzing visit data with location coordinates",
    version=settings.app_version,
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=settings.allowed_credentials,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

def get_data_file_path() -> Path:
    """Dependency to get the data file path"""
    return settings.get_data_file_path()

def validate_data_file(data_path: Path = Depends(get_data_file_path)) -> Path:
    """Dependency to validate data file exists"""
    if not data_path.exists():
        raise HTTPException(
            status_code=404, 
            detail=f"Data file not found: {data_path}"
        )
    return data_path

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"{settings.app_name} is running", 
        "version": settings.app_version,
        "debug": settings.debug,
        "data_file": str(settings.get_data_file_path()),
        "env_data_path": settings.data_file_path
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": settings.app_name,
        "version": settings.app_version
    }

@app.get("/api/visits", response_model=VisitResponse)
async def get_visits(
    limit: Optional[int] = Query(
        settings.max_records_per_request, 
        ge=1, 
        le=settings.max_records_per_request
    ),
    offset: Optional[int] = Query(0, ge=0),
    place: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    data_path: Path = Depends(validate_data_file)
):
    """Get visit records with optional filtering"""
    try:
        # Load all records first using concurrent processing
        all_records = load_visits_from_csv(str(data_path))
        
        # Apply filters
        filtered_records = all_records
        
        if place:
            filtered_records = [r for r in filtered_records if place.lower() in r.place.lower()]
        
        if start_date:
            start_dt = pd.to_datetime(start_date)
            filtered_records = [r for r in filtered_records if r.timestamp >= start_dt]
        
        if end_date:
            end_dt = pd.to_datetime(end_date)
            filtered_records = [r for r in filtered_records if r.timestamp <= end_dt]
        
        # Apply pagination
        total = len(filtered_records)
        paginated_records = filtered_records[offset:offset + limit]
        
        logger.info(f"Retrieved {len(paginated_records)} records from {total} total")
        
        return VisitResponse(
            success=True,
            data=paginated_records,
            total=total
        )
        
    except Exception as e:
        logger.error(f"Error loading visits data: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.host, 
        port=settings.port, 
        reload=settings.debug
    )
