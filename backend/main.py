from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import os
from api.routes import assistant, auth, projects
from core.config import settings, is_production
from core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="AI Personal Assistant",
    description="AI-powered personal assistant with MCP integration",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware - more permissive in development
if is_production():
    # Production CORS settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://your-netlify-site.netlify.app",  # Update with your Netlify URL
            "https://your-render-app.onrender.com"    # Update with your Render URL
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # Development CORS settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(assistant.router, prefix="/api/assistant", tags=["assistant"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])

@app.get("/")
async def root():
    return {"message": "AI Personal Assistant API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Personal Assistant"}

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv("PORT", settings.port))
    host = os.getenv("HOST", settings.host)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=not is_production()  # Only reload in development
    )
