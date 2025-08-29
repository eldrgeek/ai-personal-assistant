from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Application
    app_name: str = "AI Personal Assistant"
    app_version: str = "0.1.0"
    debug: bool = True
    
    # Database - Use absolute path to ensure it works from any directory
    database_url: str = "sqlite:///./backend/ai_assistant.db"
    
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
    
    # Production settings
    port: int = 8000
    host: str = "0.0.0.0"
    
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

# Production environment detection
def is_production():
    """Check if running in production environment"""
    # Multiple ways to detect production
    env_var = os.getenv("ENVIRONMENT", "").lower()
    render_service = os.getenv("RENDER_SERVICE_NAME")  # Render sets this automatically
    port = os.getenv("PORT", "")  # Render typically sets this to 10000
    
    # If we're on Render (RENDER_SERVICE_NAME exists) or PORT is 10000, assume production
    if render_service or port == "10000":
        return True
    
    # Fallback to ENVIRONMENT variable
    return env_var == "production"

# Update settings based on environment
if is_production():
    settings.debug = False
    settings.host = "0.0.0.0"
    # In production, use environment variables for sensitive data
    if os.getenv("SECRET_KEY"):
        settings.secret_key = os.getenv("SECRET_KEY")
    if os.getenv("DATABASE_URL"):
        settings.database_url = os.getenv("DATABASE_URL")
else:
    # In development, ensure we use the correct database path
    # Find the project root by looking for the backend directory
    current_working_dir = os.getcwd()
    
    # If we're already in the backend directory, go up one level
    if os.path.basename(current_working_dir) == "backend":
        project_root = os.path.dirname(current_working_dir)
    else:
        # Otherwise, assume we're in the project root
        project_root = current_working_dir
    
    db_path = os.path.join(project_root, "backend", "ai_assistant.db")
    settings.database_url = f"sqlite:///{db_path}"

# Load environment variables on import
load_env()
