from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()


class Project(BaseModel):
    id: str
    name: str
    description: str
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime


class ProjectCreate(BaseModel):
    name: str
    description: str
    priority: str = "medium"


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None


# Mock projects data (in real app, this would come from database)
MOCK_PROJECTS = [
    {
        "id": "1",
        "name": "MCP connection to assistant",
        "description": "Integrate MCP server with personal assistant",
        "priority": "high",
        "status": "in_progress",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": "2",
        "name": "Assistant v0",
        "description": "Rituals, sprints, logging system",
        "priority": "medium",
        "status": "active",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": "3",
        "name": "Improve Reminder Attention-Grabbing",
        "description": "Enhance reminder system effectiveness",
        "priority": "medium",
        "status": "planned",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": "4",
        "name": "Inbox Zero",
        "description": "Daily email triage to zero",
        "priority": "high",
        "status": "daily",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": "5",
        "name": "Advertisements for Chi Life",
        "description": "Create marketing materials for Chi Life",
        "priority": "medium",
        "status": "planned",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": "6",
        "name": "Flyers, cards, etc. for Chi Life",
        "description": "Print materials for Chi Life business",
        "priority": "medium",
        "status": "planned",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": "7",
        "name": "CJ Clarke for City Council",
        "description": "Campaign support for CJ Clarke",
        "priority": "medium",
        "status": "active",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": "8",
        "name": "NBA Connect for Greg Foster",
        "description": "Retired player portal development",
        "priority": "medium",
        "status": "active",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": "9",
        "name": "Discord+ with Mark and James",
        "description": "Enhanced Discord integration project",
        "priority": "low",
        "status": "planned",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": "10",
        "name": "Build the Personal Assistant app",
        "description": "Develop the main personal assistant application",
        "priority": "high",
        "status": "in_progress",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


@router.get("/", response_model=List[Project])
async def get_projects():
    """Get all projects"""
    return MOCK_PROJECTS


@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: str):
    """Get a specific project by ID"""
    for project in MOCK_PROJECTS:
        if project["id"] == project_id:
            return project
    raise HTTPException(status_code=404, detail="Project not found")


@router.post("/", response_model=Project)
async def create_project(project: ProjectCreate):
    """Create a new project"""
    new_project = {
        "id": str(len(MOCK_PROJECTS) + 1),
        "name": project.name,
        "description": project.description,
        "priority": project.priority,
        "status": "planned",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_PROJECTS.append(new_project)
    return new_project


@router.put("/{project_id}", response_model=Project)
async def update_project(project_id: str, project_update: ProjectUpdate):
    """Update an existing project"""
    for i, project in enumerate(MOCK_PROJECTS):
        if project["id"] == project_id:
            # Update only provided fields
            if project_update.name is not None:
                project["name"] = project_update.name
            if project_update.description is not None:
                project["description"] = project_update.description
            if project_update.priority is not None:
                project["priority"] = project_update.priority
            if project_update.status is not None:
                project["status"] = project_update.status
            
            project["updated_at"] = datetime.now()
            MOCK_PROJECTS[i] = project
            return project
    
    raise HTTPException(status_code=404, detail="Project not found")


@router.delete("/{project_id}")
async def delete_project(project_id: str):
    """Delete a project"""
    for i, project in enumerate(MOCK_PROJECTS):
        if project["id"] == project_id:
            deleted_project = MOCK_PROJECTS.pop(i)
            return {"message": f"Project '{deleted_project['name']}' deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Project not found")


@router.get("/priority/{priority}")
async def get_projects_by_priority(priority: str):
    """Get projects filtered by priority"""
    filtered_projects = [p for p in MOCK_PROJECTS if p["priority"] == priority.lower()]
    return filtered_projects


@router.get("/status/{status}")
async def get_projects_by_status(status: str):
    """Get projects filtered by status"""
    filtered_projects = [p for p in MOCK_PROJECTS if p["status"] == status.lower()]
    return filtered_projects
