from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
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
    # IMPORTANT: Only exact origin strings work with credentials=True
    # FastAPI doesn't support wildcard patterns like "https://*.netlify.app"
    allowed_origins = [
        "https://mikes-personal-assistant.netlify.app",  # Primary Netlify URL
        "https://ai-personal-assistant-9xpq.onrender.com"  # Backend self-reference
    ]
    allow_credentials = True
else:
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000", 
        "http://127.0.0.1:5173"
    ]
    allow_credentials = True

logger.info(f"Allowed CORS origins: {allowed_origins}")
logger.info(f"Allow credentials: {allow_credentials}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allow_credentials,
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
    return {"message": "AI Personal Assistant API", "version": "0.1.0", "build": "87bb345-v2"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "service": "AI Personal Assistant"}

@app.get("/debug/cors")
async def debug_cors():
    """Debug endpoint to check CORS configuration"""
    logger.info("CORS debug endpoint accessed")
    return {
        "is_production": is_production(),
        "environment": os.getenv("ENVIRONMENT", "not-set"),
        "allowed_origins": allowed_origins,
        "allow_credentials": allow_credentials
    }

@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str):
    """
    Handle CORS preflight requests explicitly
    """
    origin = request.headers.get("origin")
    logger.info(f"Preflight request from origin: {origin} for path: /{rest_of_path}")
    
    response_headers = {
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Max-Age": "3600",
    }
    
    # Check if origin is allowed
    if is_production():
        allowed = [
            "https://mikes-personal-assistant.netlify.app",
            "https://ai-personal-assistant-9xpq.onrender.com"
        ]
    else:
        allowed = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173"
        ]
    
    if origin in allowed:
        response_headers["Access-Control-Allow-Origin"] = origin
        response_headers["Access-Control-Allow-Credentials"] = "true"
        logger.info(f"CORS approved for origin: {origin}")
    else:
        logger.warning(f"CORS rejected for origin: {origin}")
    
    return Response(headers=response_headers)

@app.get("/test/cors")
async def test_cors():
    """Simple test endpoint for CORS verification"""
    logger.info("CORS test endpoint accessed")
    return {
        "status": "success",
        "message": "CORS is working correctly",
        "timestamp": os.popen('date').read().strip(),
        "backend_url": "https://ai-personal-assistant-9xpq.onrender.com"
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
