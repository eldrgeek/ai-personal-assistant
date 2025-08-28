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
from models import Sprint, SprintDistraction, Project, Ritual, RitualStep
from utils.seed_data import seed_all_data

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
    
    # Seed initial data
    try:
        seed_all_data()
        logger.info("Initial data seeding completed")
    except Exception as e:
        logger.error(f"Data seeding failed: {e}")
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
    # Get current git revision
    try:
        import subprocess
        git_rev = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], 
                                        stderr=subprocess.DEVNULL).decode().strip()
    except:
        git_rev = "unknown"
    
    return {
        "message": "AI Personal Assistant API", 
        "version": "0.1.0", 
        "build": f"{git_rev}-v4",
        "deploy_time": __import__('datetime').datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "service": "AI Personal Assistant"}

@app.get("/debug/cors")
async def debug_cors():
    """Debug endpoint to check CORS configuration"""
    logger.info("CORS debug endpoint accessed")
    
    # Get git revision info
    import subprocess
    try:
        git_rev = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], 
                                        stderr=subprocess.DEVNULL).decode().strip()
        git_branch = subprocess.check_output(['git', 'branch', '--show-current'], 
                                           stderr=subprocess.DEVNULL).decode().strip()
    except:
        git_rev = "unknown"
        git_branch = "unknown"
    
    # Categorize environment variables
    production_indicators = {
        "RENDER_SERVICE_NAME": os.getenv("RENDER_SERVICE_NAME"),
        "RENDER_SERVICE_ID": os.getenv("RENDER_SERVICE_ID"), 
        "RENDER": os.getenv("RENDER"),
        "PORT": os.getenv("PORT"),
        "ENVIRONMENT": os.getenv("ENVIRONMENT"),
        "NODE_ENV": os.getenv("NODE_ENV"),
        "PYTHON_ENV": os.getenv("PYTHON_ENV")
    }
    
    # Filter out None values and common system vars
    system_vars = {}
    custom_vars = {}
    for key, value in os.environ.items():
        if key.startswith(('PATH', 'HOME', 'USER', 'SHELL', 'PWD', 'OLDPWD', 'TERM', 'LANG')):
            continue  # Skip common system vars
        elif key.startswith(('RENDER_', 'RAILWAY_', 'HEROKU_', 'VERCEL_', 'NETLIFY_')):
            system_vars[key] = value
        else:
            custom_vars[key] = value
    
    return {
        "deployment_info": {
            "git_revision": git_rev,
            "git_branch": git_branch,
            "build_version": "b34eb02-v3",  # Update this with each deploy
            "timestamp": __import__('datetime').datetime.now().isoformat()
        },
        "environment_analysis": {
            "is_production": is_production(),
            "production_indicators": {k: v for k, v in production_indicators.items() if v is not None},
            "platform_vars": system_vars,
            "custom_vars": custom_vars
        },
        "cors_configuration": {
            "allowed_origins": allowed_origins,
            "allow_credentials": allow_credentials,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "headers": ["*"]
        },
        "system_info": {
            "python_version": __import__('sys').version,
            "platform": __import__('platform').platform(),
            "working_directory": os.getcwd()
        }
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
