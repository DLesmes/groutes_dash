"""
Utilities for handling CSV data
"""
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

# Add the backend directory to Python path for imports
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from models.visits import VisitRecord

def parse_coordinates_batch(coordinates_series: pd.Series) -> tuple:
    """
    Parse coordinates from a pandas Series using vectorized operations
    
    Args:
        coordinates_series: Pandas Series with coordinate strings
        
    Returns:
        Tuple of (latitudes, longitudes) as numpy arrays
    """
    # Create empty arrays
    latitudes = np.full(len(coordinates_series), np.nan)
    longitudes = np.full(len(coordinates_series), np.nan)
    
    # Vectorized parsing
    for idx, coord_str in enumerate(coordinates_series):
        try:
            # Try comma separator first, then space separator
            if ',' in str(coord_str):
                coords = str(coord_str).strip().split(',')
            else:
                coords = str(coord_str).strip().split()
            
            if len(coords) == 2:
                lat, lon = float(coords[0]), float(coords[1])
                # Validate coordinates
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    latitudes[idx] = lat
                    longitudes[idx] = lon
        except (ValueError, IndexError):
            continue
    
    return latitudes, longitudes

def process_chunk(chunk: pd.DataFrame) -> List[VisitRecord]:
    """
    Process a chunk of data and convert to VisitRecord objects
    
    Args:
        chunk: DataFrame chunk to process
        
    Returns:
        List of VisitRecord objects
    """
    try:
        # Parse coordinates in batch
        latitudes, longitudes = parse_coordinates_batch(chunk['point'])
        
        # Convert to records - use enumerate instead of chunk.index
        records = []
        for local_idx, (_, row) in enumerate(chunk.iterrows()):
            try:
                record = VisitRecord(
                    timestamp=pd.to_datetime(row['timestamp']),
                    point=str(row['point']),
                    place=str(row['place']),
                    latitude=latitudes[local_idx] if not np.isnan(latitudes[local_idx]) else None,
                    longitude=longitudes[local_idx] if not np.isnan(longitudes[local_idx]) else None
                )
                records.append(record)
            except Exception as e:
                print(f"Error parsing row in chunk: {e}")
                continue
        
        return records
    except Exception as e:
        print(f"Error processing chunk: {e}")
        return []

def load_visits_from_csv(file_path: str, limit: Optional[int] = None, chunk_size: int = 5000) -> List[VisitRecord]:
    """
    Load visit records from CSV file using pandas and concurrent processing
    
    Args:
        file_path: Path to the CSV file
        limit: Maximum number of records to load
        chunk_size: Size of chunks for concurrent processing
        
    Returns:
        List of VisitRecord objects
    """
    try:
        # Read CSV with pandas
        df = pd.read_csv(file_path)
        
        if limit:
            df = df.head(limit)
        
        # If dataset is small, process directly
        if len(df) <= chunk_size:
            return process_chunk(df)
        
        # Split into chunks for concurrent processing
        chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]
        
        all_records = []
        
        # Use ThreadPoolExecutor for concurrent processing
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all chunks for processing
            future_to_chunk = {executor.submit(process_chunk, chunk): chunk for chunk in chunks}
            
            # Collect results as they complete
            for future in as_completed(future_to_chunk):
                try:
                    chunk_records = future.result()
                    all_records.extend(chunk_records)
                except Exception as e:
                    print(f"Error processing chunk: {e}")
                    continue
        
        return all_records
        
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []
