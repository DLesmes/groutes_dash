from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import pandas as pd
from pathlib import Path
import logging

# Import from the new structure
from models.visits import VisitRecord, VisitResponse, LocationStats, FilterParams
from utils.csv_utils import (
    examine_csv_structure, 
    load_visits_from_csv, 
    get_coordinate_statistics,
    get_unique_places_from_csv
)
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

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Data file: {settings.get_data_file_path()}")
    
    # Log settings warnings
    warnings = settings.validate_settings()
    for warning in warnings:
        logger.warning(warning)

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Shutting down application")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"{settings.app_name} is running", 
        "version": settings.app_version,
        "debug": settings.debug,
        "data_file": str(settings.get_data_file_path())
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": settings.app_name,
        "version": settings.app_version
    }

@app.get("/api/config")
async def get_config():
    """Get application configuration (non-sensitive)"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "max_records_per_request": settings.max_records_per_request,
        "cache_enabled": settings.cache_enabled,
        "allowed_origins": settings.allowed_origins
    }

@app.get("/api/structure")
async def get_data_structure(data_path: Path = Depends(validate_data_file)):
    """Get information about the CSV data structure"""
    try:
        structure = examine_csv_structure(str(data_path))
        return {"success": True, "structure": structure}
    except Exception as e:
        logger.error(f"Error examining data structure: {e}")
        raise HTTPException(status_code=500, detail=f"Error examining data structure: {str(e)}")

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
        # Load all records first
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

@app.get("/api/visits/stats", response_model=LocationStats)
async def get_visit_statistics(data_path: Path = Depends(validate_data_file)):
    """Get statistics about the visit data"""
    try:
        records = load_visits_from_csv(str(data_path))
        
        if not records:
            return LocationStats(
                total_visits=0,
                unique_places=0,
                date_range={"start": None, "end": None},
                coordinates_summary={"valid_coordinates": 0, "invalid_coordinates": 0}
            )
        
        # Calculate statistics
        unique_places = len(set(r.place for r in records))
        date_range = {
            "start": min(r.timestamp for r in records).isoformat(),
            "end": max(r.timestamp for r in records).isoformat()
        }
        
        coord_stats = get_coordinate_statistics(records)
        
        logger.info(f"Calculated statistics for {len(records)} records")
        
        return LocationStats(
            total_visits=len(records),
            unique_places=unique_places,
            date_range=date_range,
            coordinates_summary=coord_stats
        )
        
    except Exception as e:
        logger.error(f"Error calculating statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")

@app.get("/api/visits/{record_id}")
async def get_visit_by_id(
    record_id: int,
    data_path: Path = Depends(validate_data_file)
):
    """Get a specific visit record by ID (index)"""
    try:
        records = load_visits_from_csv(str(data_path))
        
        if record_id < 0 or record_id >= len(records):
            raise HTTPException(
                status_code=404, 
                detail=f"Record ID {record_id} out of range (0-{len(records)-1})"
            )
        
        return {"success": True, "data": records[record_id]}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error loading record {record_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading record: {str(e)}")

@app.get("/api/places")
async def get_unique_places(data_path: Path = Depends(validate_data_file)):
    """Get list of unique places"""
    try:
        places = get_unique_places_from_csv(str(data_path))
        
        return {
            "success": True,
            "places": places,
            "count": len(places)
        }
        
    except Exception as e:
        logger.error(f"Error getting unique places: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting places: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.host, 
        port=settings.port, 
        reload=settings.debug
    )
