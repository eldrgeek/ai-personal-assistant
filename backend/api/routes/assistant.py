from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import httpx
from core.config import settings
from core.database import get_db_session
from models import Sprint, SprintDistraction
from sqlalchemy.orm import Session

router = APIRouter()


class SprintRequest(BaseModel):
    task: str
    duration_minutes: int
    description: Optional[str] = None


class SprintResponse(BaseModel):
    id: str
    task: str
    duration_minutes: int
    start_time: datetime
    end_time: datetime
    status: str
    distractions: List[str] = []


class MCPToolRequest(BaseModel):
    tool_name: str
    parameters: dict


@router.post("/sprint/start", response_model=SprintResponse)
async def start_sprint(request: SprintRequest, db: Session = Depends(get_db_session)):
    """Start a new sprint session"""
    try:
        # Create sprint session
        start_time = datetime.now()
        end_time = start_time.replace(minute=start_time.minute + request.duration_minutes)
        
        # Create Sprint object and save to database
        sprint = Sprint(
            task=request.task,
            description=request.description,
            duration_minutes=request.duration_minutes,
            start_time=start_time,
            end_time=end_time,
            status="active"
        )
        
        db.add(sprint)
        db.commit()
        db.refresh(sprint)
        
        # Return response
        return SprintResponse(
            id=sprint.id,
            task=sprint.task,
            duration_minutes=sprint.duration_minutes,
            start_time=sprint.start_time,
            end_time=sprint.end_time,
            status=sprint.status,
            distractions=[]
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to start sprint: {str(e)}")


@router.get("/sprint/active")
async def get_active_sprint(db: Session = Depends(get_db_session)):
    """Get the currently active sprint"""
    try:
        active_sprint = db.query(Sprint).filter(Sprint.status == "active").order_by(Sprint.created_at.desc()).first()
        if not active_sprint:
            return {"message": "No active sprint"}
        
        # Get distractions for this sprint
        distractions = [d.distraction for d in active_sprint.distractions]
        
        return SprintResponse(
            id=active_sprint.id,
            task=active_sprint.task,
            duration_minutes=active_sprint.duration_minutes,
            start_time=active_sprint.start_time,
            end_time=active_sprint.end_time,
            status=active_sprint.status,
            distractions=distractions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get active sprint: {str(e)}")


@router.get("/sprint/all")
async def get_all_sprints(db: Session = Depends(get_db_session)):
    """Get all sprints"""
    try:
        sprints = db.query(Sprint).order_by(Sprint.created_at.desc()).all()
        return [
            SprintResponse(
                id=sprint.id,
                task=sprint.task,
                duration_minutes=sprint.duration_minutes,
                start_time=sprint.start_time,
                end_time=sprint.end_time,
                status=sprint.status,
                distractions=[d.distraction for d in sprint.distractions]
            )
            for sprint in sprints
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sprints: {str(e)}")


@router.post("/sprint/{sprint_id}/nudge")
async def sprint_nudge(sprint_id: str, message: str = "15-minute nudge", db: Session = Depends(get_db_session)):
    """Send a mid-sprint nudge"""
    try:
        sprint = db.query(Sprint).filter(Sprint.id == sprint_id).first()
        if not sprint:
            raise HTTPException(status_code=404, detail="Sprint not found")
        
        return {
            "sprint_id": sprint_id,
            "nudge_time": datetime.now(),
            "message": message,
            "task": sprint.task,
            "remaining_minutes": max(0, (sprint.end_time - datetime.now()).total_seconds() / 60)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send nudge: {str(e)}")


@router.post("/sprint/{sprint_id}/distraction")
async def log_distraction(sprint_id: str, distraction: str, db: Session = Depends(get_db_session)):
    """Log a distraction during sprint"""
    try:
        sprint = db.query(Sprint).filter(Sprint.id == sprint_id).first()
        if not sprint:
            raise HTTPException(status_code=404, detail="Sprint not found")
        
        # Create and save distraction
        distraction_obj = SprintDistraction(
            sprint_id=sprint_id,
            distraction=distraction
        )
        
        db.add(distraction_obj)
        db.commit()
        
        return {
            "sprint_id": sprint_id,
            "distraction": distraction,
            "timestamp": distraction_obj.timestamp,
            "id": distraction_obj.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to log distraction: {str(e)}")


@router.post("/sprint/{sprint_id}/complete")
async def complete_sprint(sprint_id: str, retro: str, db: Session = Depends(get_db_session)):
    """Complete a sprint with retrospective"""
    try:
        sprint = db.query(Sprint).filter(Sprint.id == sprint_id).first()
        if not sprint:
            raise HTTPException(status_code=404, detail="Sprint not found")
        
        # Update sprint status
        sprint.status = "completed"
        sprint.retrospective = retro
        sprint.actual_end_time = datetime.now()
        sprint.updated_at = datetime.now()
        
        db.commit()
        
        return {
            "sprint_id": sprint_id,
            "completion_time": sprint.actual_end_time,
            "retrospective": retro,
            "status": "completed",
            "task": sprint.task
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to complete sprint: {str(e)}")


@router.post("/mcp/tool")
async def execute_mcp_tool(request: MCPToolRequest):
    """Execute an MCP tool"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.mcp_server_url}/tool",
                json={
                    "tool": request.tool_name,
                    "parameters": request.parameters
                },
                headers={
                    "Authorization": f"Bearer {settings.mcp_auth_token}" if settings.mcp_auth_token else ""
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"MCP tool execution failed: {response.text}"
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute MCP tool: {str(e)}")


@router.get("/rituals/morning")
async def get_morning_ritual():
    """Get morning ritual checklist"""
    return {
        "ritual": "Morning Ritual",
        "steps": [
            "Cold shower",
            "Put on Limitless AI pendant",
            "Quick project/meeting review",
            "Journaling (gratitude + focus + visualization/affirmation)"
        ],
        "estimated_duration": "20 minutes"
    }


@router.get("/rituals/evening")
async def get_evening_ritual():
    """Get evening ritual checklist"""
    return {
        "ritual": "Evening Ritual",
        "steps": [
            "Charge all devices (including pendant)",
            "Retro journaling (3 wins + 1 lesson + tomorrow's focus)",
            "Looking ahead: pick tomorrow's focus"
        ],
        "estimated_duration": "15 minutes"
    }


@router.get("/family/reminders")
async def get_family_reminders():
    """Get family-related reminders"""
    return {
        "daily_tasks": [
            "6:00 PM: Reach out to kids (Daniel, Mira, Alyssa) and granddaughter Kaya"
        ],
        "family_members": {
            "children": ["Dana", "Mira", "Alyssa"],
            "grandchildren": ["Kyra", "Siena", "Kaya", "Luke", "Taz", "Michael", "Sylvia"],
            "siblings": ["Mark", "Zorina"]
        }
    }
