"""
Configuration settings from environment variables.
Uses python-dotenv to load settings from .env file.
"""

import os
import logging
from typing import List
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load .env file from backend directory
backend_dir = Path(__file__).parent
env_file_path = backend_dir / ".env"

if env_file_path.exists():
    load_dotenv(dotenv_path=env_file_path)
    logger.info(f"Loaded configuration from {env_file_path}")
else:
    load_dotenv()
    logger.warning(f".env file not found at {env_file_path}")

class Settings:
    """Application settings."""
    
    # Application
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./contact_messages.db"
    )
    
    # SMTP Configuration
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "True").lower() == "true"
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", os.getenv("SMTP_USER", ""))
    
    # Owner email (where notifications are sent)
    OWNER_EMAIL: str = os.getenv("OWNER_EMAIL", "")
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        origin.strip() 
        for origin in os.getenv("ALLOWED_ORIGINS", "https://aravindadityxa.github.io,http://localhost:5500,http://127.0.0.1:5500").split(",")
    ]
    
    # Rate Limiting
    RATE_LIMIT_MAX_REQUESTS: int = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "5"))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "3600"))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    def __init__(self):
        """Validate required settings."""
        # Validate required SMTP settings
        if not self.SMTP_USER or not self.SMTP_PASSWORD:
            raise ValueError("SMTP_USER and SMTP_PASSWORD must be set in .env")
        
        if not self.OWNER_EMAIL:
            raise ValueError("OWNER_EMAIL must be set in .env")
        
        # Check for placeholder values
        if "YOUR_" in self.SMTP_PASSWORD:
            raise ValueError(
                "SMTP_PASSWORD is a placeholder. "
                "Please set your actual Gmail App Password in .env"
            )
        
        logger.debug(f"Settings loaded: environment={self.ENVIRONMENT}, debug={self.DEBUG}")


# Create global settings instance
try:
    settings = Settings()
    logger.info("Configuration initialized successfully")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise
