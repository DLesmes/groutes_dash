"""
Utilities for handling CSV data
"""
import pandas as pd
from typing import Optional, List, Any

def load_visits_from_df(
    df: pd.DataFrame,
    place: Optional[str] = None,
    start_date: Optional[Any] = None,  # Accepts date, datetime, or str
    end_date: Optional[Any] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None
) -> List[dict]:
    """
    Filter visit records from a DataFrame, returning a list of dicts.
    """
    try:
        # Always parse as datetime and remove timezone info
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        if hasattr(df['timestamp'].dt, 'tz'):
            df['timestamp'] = df['timestamp'].dt.tz_localize(None)

        if df['timestamp'].isnull().any():
            raise ValueError("Some timestamps could not be parsed.")

        # Filtering
        if place:
            df = df[df['place'].str.contains(place, case=False, na=False)].copy()
        if start_date:
            start = pd.to_datetime(start_date)
            if getattr(start, 'tzinfo', None) is not None:
                start = start.replace(tzinfo=None)
            df = df[df['timestamp'] >= start].copy()
        if end_date:
            end = pd.to_datetime(end_date)
            if getattr(end, 'tzinfo', None) is not None:
                end = end.replace(tzinfo=None)
            df = df[df['timestamp'] <= end].copy()

        # Pagination
        if offset:
            df = df.iloc[offset:].copy()
        if limit:
            df = df.iloc[:limit].copy()

        return df.to_dict(orient='records')
    except Exception as e:
        # Raise a clear error for FastAPI to catch
        raise RuntimeError(f"Error loading data: {e}")
