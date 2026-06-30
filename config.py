# config.py
import os
from pathlib import Path

class Config:
    """Application configuration"""
    
    # File upload settings
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}
    
    # LLM settings
    DEFAULT_MODEL = "llama3-70b-8192"
    TEMPERATURE = 0.3
    MAX_TOKENS = 4096
    
    # Paths
    BASE_DIR = Path(__file__).parent
    UPLOAD_DIR = BASE_DIR / "uploads"
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories"""
        cls.UPLOAD_DIR.mkdir(exist_ok=True)