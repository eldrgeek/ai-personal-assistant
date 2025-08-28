from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import os
import logging
from api.routes import assistant, auth, projects
from core.config import settings, is_production
from core.database import init_db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting AI Personal Assistant...")
    logger.info(f"Environment: {'production' if is_production() else 'development'}")
    logger.info(f"Debug mode: {settings.debug}")
    await init_db()
    logger.info("Database initialized successfully")
    yield
    # Shutdown
    logger.info("Shutting down AI Personal Assistant...")
    pass


app = FastAPI(
    title="AI Personal Assistant",
    description="AI-powered personal assistant with MCP integration",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware configuration
logger.info("Configuring CORS middleware...")
logger.info(f"Production environment detected: {is_production()}")

# Define allowed origins based on environment
if is_production():
    allowed_origins = [
        "https://mikes-personal-assistant.netlify.app",
        "https://ai-personal-assistant-9xpq.onrender.com",
        "https://netlify.app",  # Allow all netlify subdomains
        "*"  # Temporarily allow all origins for debugging
    ]
else:
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"  # Allow all in development
    ]

logger.info(f"Allowed CORS origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

logger.info("CORS middleware configured successfully")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(assistant.router, prefix="/api/assistant", tags=["assistant"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "AI Personal Assistant API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "service": "AI Personal Assistant"}

@app.get("/debug/cors")
async def debug_cors():
    """Debug endpoint to check CORS configuration"""
    logger.info("CORS debug endpoint accessed")
    
    # Get the current allowed origins based on environment
    if is_production():
        current_origins = [
            "https://mikes-personal-assistant.netlify.app",
            "https://ai-personal-assistant-9xpq.onrender.com",
            "https://netlify.app",
            "*"
        ]
    else:
        current_origins = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "*"
        ]
    
    return {
        "cors_enabled": True,
        "allow_origins": current_origins,
        "environment": "production" if is_production() else "development",
        "debug_mode": settings.debug,
        "is_production": is_production(),
        "env_vars": {
            "ENVIRONMENT": os.getenv("ENVIRONMENT"),
            "PORT": os.getenv("PORT"),
            "HOST": os.getenv("HOST")
        }
    }

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv("PORT", settings.port))
    host = os.getenv("HOST", settings.host)
    
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=not is_production()  # Only reload in development
    )
