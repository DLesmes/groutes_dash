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
