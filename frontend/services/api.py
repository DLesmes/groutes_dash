import requests

BACKEND_URL = "http://backend:8000"  # Use "http://localhost:8000" for local dev

def get_visits_by_date(date):
    try:
        resp = requests.get(f"{BACKEND_URL}/api/visits", params={"end_date": date})
        resp.raise_for_status()
        return resp.json().get("data", [])
    except Exception as e:
        return []
