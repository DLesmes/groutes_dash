"""
Utilities for handling CSV data
"""
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
import sys

# Add the backend directory to Python path for imports
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from models.visits import VisitRecord, Location

def examine_csv_structure(file_path: str) -> Dict[str, Any]:
    """
    Examine the structure of the CSV file
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Dictionary with CSV structure information
    """
    try:
        # Read first few rows to understand structure
        df = pd.read_csv(file_path, nrows=5)
        
        info = {
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.to_dict(),
            "shape": df.shape,
            "sample_data": df.head(3).to_dict('records'),
            "null_counts": df.isnull().sum().to_dict()
        }
        
        # Try to read more rows to get better statistics
        df_full = pd.read_csv(file_path)
        info.update({
            "total_rows": len(df_full),
            "total_columns": len(df_full.columns),
            "date_range": None,
            "unique_places": None
        })
        
        # Check if timestamp column exists and get date range
        if 'timestamp' in df_full.columns:
            try:
                df_full['timestamp'] = pd.to_datetime(df_full['timestamp'])
                info['date_range'] = {
                    'start': df_full['timestamp'].min().isoformat(),
                    'end': df_full['timestamp'].max().isoformat()
                }
            except Exception as e:
                info['timestamp_error'] = str(e)
        
        # Check unique places
        if 'place' in df_full.columns:
            info['unique_places'] = df_full['place'].nunique()
        
        return info
        
    except Exception as e:
        return {"error": str(e)}

def load_visits_from_csv(file_path: str, limit: Optional[int] = None) -> List[VisitRecord]:
    """
    Load visit records from CSV file
    
    Args:
        file_path: Path to the CSV file
        limit: Maximum number of records to load
        
    Returns:
        List of VisitRecord objects
    """
    try:
        # Read CSV with pandas
        df = pd.read_csv(file_path)
        
        if limit:
            df = df.head(limit)
        
        records = []
        for _, row in df.iterrows():
            try:
                record = VisitRecord(
                    timestamp=pd.to_datetime(row['timestamp']),
                    point=str(row['point']),
                    place=str(row['place'])
                )
                records.append(record)
            except Exception as e:
                print(f"Error parsing row {_}: {e}")
                continue
        
        return records
        
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []

def validate_coordinate_format(point_string: str) -> bool:
    """
    Validate if a coordinate string is in the expected format
    
    Args:
        point_string: String with coordinates
        
    Returns:
        True if valid format, False otherwise
    """
    try:
        Location.from_string(point_string)
        return True
    except ValueError:
        return False

def get_coordinate_statistics(records: List[VisitRecord]) -> Dict[str, Any]:
    """
    Get statistics about coordinate data
    
    Args:
        records: List of visit records
        
    Returns:
        Dictionary with coordinate statistics
    """
    valid_locations = [r.location for r in records if r.location is not None]
    invalid_coordinates = [r.point for r in records if r.location is None]
    
    stats = {
        "total_records": len(records),
        "valid_coordinates": len(valid_locations),
        "invalid_coordinates": len(invalid_coordinates),
        "validity_rate": len(valid_locations) / len(records) if records else 0
    }
    
    if valid_locations:
        lats = [loc.latitude for loc in valid_locations]
        lons = [loc.longitude for loc in valid_locations]
        
        stats.update({
            "lat_range": {"min": min(lats), "max": max(lats)},
            "lon_range": {"min": min(lons), "max": max(lons)},
            "avg_lat": sum(lats) / len(lats),
            "avg_lon": sum(lons) / len(lons)
        })
    
    return stats

def export_to_csv(records: List[VisitRecord], filepath: str) -> bool:
    """
    Export visit records to CSV file
    
    Args:
        records: List of visit records
        filepath: Output file path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        data = []
        for record in records:
            data.append({
                'timestamp': record.timestamp,
                'point': record.point,
                'place': record.place,
                'latitude': record.location.latitude if record.location else None,
                'longitude': record.location.longitude if record.location else None
            })
        
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False

def get_unique_places_from_csv(file_path: str) -> List[str]:
    """
    Get unique places from CSV file
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        List of unique place names
    """
    try:
        df = pd.read_csv(file_path)
        if 'place' in df.columns:
            return sorted(df['place'].unique().tolist())
        return []
    except Exception as e:
        print(f"Error getting unique places: {e}")
        return []
