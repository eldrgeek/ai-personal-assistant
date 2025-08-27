from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Application
    app_name: str = "AI Personal Assistant"
    app_version: str = "0.1.0"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./ai_assistant.db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AI Services
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # MCP Integration
    mcp_server_url: str = "http://localhost:3001"
    mcp_auth_token: Optional[str] = None
    
    # External Services
    google_calendar_credentials: Optional[str] = None
    whatsapp_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Load environment variables
def load_env():
    """Load environment variables from .env file"""
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

# Load environment variables on import
load_env()
