from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from models.project import Project as ProjectModel
from core.database import get_db

router = APIRouter()


class Project(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    priority: str
    status: str
    category: Optional[str] = None
    progress_percentage: int
    is_high_priority: bool
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    category: Optional[str] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    progress_percentage: Optional[int] = None


@router.get("/", response_model=List[Project])
async def get_projects(db: Session = Depends(get_db)):
    """Get all projects"""
    projects = db.query(ProjectModel).all()
    return projects


@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: str, db: Session = Depends(get_db)):
    """Get a specific project by ID"""
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=Project)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project"""
    db_project = ProjectModel(
        title=project.title,
        description=project.description,
        priority=project.priority,
        category=project.category,
        status="active"
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.put("/{project_id}", response_model=Project)
async def update_project(project_id: str, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    """Update an existing project"""
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Update only provided fields
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}")
async def delete_project(project_id: str, db: Session = Depends(get_db)):
    """Delete a project"""
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_title = project.title
    db.delete(project)
    db.commit()
    return {"message": f"Project '{project_title}' deleted successfully"}


@router.get("/priority/{priority}")
async def get_projects_by_priority(priority: str, db: Session = Depends(get_db)):
    """Get projects filtered by priority"""
    projects = db.query(ProjectModel).filter(ProjectModel.priority == priority.lower()).all()
    return projects


@router.get("/status/{status}")
async def get_projects_by_status(status: str, db: Session = Depends(get_db)):
    """Get projects filtered by status"""
    projects = db.query(ProjectModel).filter(ProjectModel.status == status.lower()).all()
    return projects
