"""
Alternative settings configuration using direct environment variable access
"""
import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings loaded from environment variables"""
    
    def __init__(self):
        # Application settings
        self.app_name = os.getenv('APP_NAME', 'Visits Data API')
        self.app_version = os.getenv('APP_VERSION', '1.0.0')
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'
        
        # Server settings
        self.host = os.getenv('HOST', '0.0.0.0')
        self.port = int(os.getenv('PORT', '8000'))
        
        # Data settings
        self.data_file_path = os.getenv('DATA_FILE_PATH', 'data/99-visitas_uriel.csv')
        self.max_records_per_request = int(os.getenv('MAX_RECORDS_PER_REQUEST', '1000'))
        
        # CORS settings
        self.allowed_origins = os.getenv('ALLOWED_ORIGINS', '["http://localhost:8501", "http://frontend:8501"]')
        # Parse JSON string to list
        try:
            import json
            self.allowed_origins = json.loads(self.allowed_origins)
        except:
            self.allowed_origins = ["http://localhost:8501", "http://frontend:8501"]
        
        self.allowed_credentials = os.getenv('ALLOWED_CREDENTIALS', 'true').lower() == 'true'
        self.allowed_methods = ["*"]
        self.allowed_headers = ["*"]
        
        # Cache settings
        self.cache_enabled = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
        self.cache_ttl = int(os.getenv('CACHE_TTL', '300'))
        
        # Logging settings
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_file = os.getenv('LOG_FILE')
    
    def get_data_file_path(self) -> Path:
        """Get the full path to the data file"""
        # If it's an absolute path, use it as is
        if os.path.isabs(self.data_file_path):
            return Path(self.data_file_path)
        
        # Otherwise, make it relative to the backend directory
        backend_dir = Path(__file__).parent
        return backend_dir / self.data_file_path
    
    def validate_settings(self) -> List[str]:
        """Validate settings and return list of warnings"""
        warnings = []
        
        # Check if data file exists
        data_path = self.get_data_file_path()
        if not data_path.exists():
            warnings.append(f"Data file not found: {data_path}")
        
        return warnings

# Create global settings instance
settings = Settings()

# Validate settings on import
warnings = settings.validate_settings()
if warnings:
    print("Settings warnings:")
    for warning in warnings:
        print(f"  ⚠️  {warning}")
