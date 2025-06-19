from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pathlib import Path
from datetime import date, timedelta
from contextlib import asynccontextmanager
import pandas as pd

from settings import settings
from services.filtering_visits import FilteringVisits

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the CSV once at startup
    app.state.visits_df = pd.read_csv(settings.get_data_file_path())
    yield
    # (Optional) Cleanup code here

app = FastAPI(
    title=settings.app_name,
    description="API for managing and analyzing visit data with location coordinates",
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=settings.allowed_credentials,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

def get_data_file_path() -> Path:
    return settings.get_data_file_path()

def validate_data_file(data_path: Path = Depends(get_data_file_path)) -> Path:
    if not data_path.exists():
        raise HTTPException(
            status_code=404, 
            detail=f"Data file not found: {data_path}"
        )
    return data_path

@app.get("/")
async def root():
    return {
        "message": f"{settings.app_name} is running", 
        "version": settings.app_version,
        "debug": settings.debug,
        "data_file": str(settings.get_data_file_path()),
        "env_data_path": settings.data_file_path
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": settings.app_name,
        "version": settings.app_version
    }

@app.get("/api/visits")
async def get_visits(
    end_date: date = Query(date(2014, 6, 11), description="Date to filter (YYYY-MM-DD)"),
    limit: Optional[int] = Query(settings.max_records_per_request, ge=1, le=settings.max_records_per_request),
    offset: Optional[int] = Query(0, ge=0),
    place: Optional[str] = Query(None),
    data_path: Path = Depends(validate_data_file)
):
    # 1-day window: start_date = end_date
    start_date = end_date

    try:
        records = FilteringVisits.filter(
            app.state.visits_df.copy(),
            place=place,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset
        )
        return {"success": True, "data": records, "total": len(records)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.host, 
        port=settings.port, 
        reload=settings.debug
    )
