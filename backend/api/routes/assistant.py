from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import httpx
from core.config import settings

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
async def start_sprint(request: SprintRequest):
    """Start a new sprint session"""
    try:
        # Create sprint session
        sprint_id = f"sprint_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_time = datetime.now()
        end_time = start_time.replace(minute=start_time.minute + request.duration_minutes)
        
        sprint = SprintResponse(
            id=sprint_id,
            task=request.task,
            duration_minutes=request.duration_minutes,
            start_time=start_time,
            end_time=end_time,
            status="active"
        )
        
        return sprint
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start sprint: {str(e)}")


@router.post("/sprint/{sprint_id}/nudge")
async def sprint_nudge(sprint_id: str, message: str = "15-minute nudge"):
    """Send a mid-sprint nudge"""
    return {
        "sprint_id": sprint_id,
        "nudge_time": datetime.now(),
        "message": message
    }


@router.post("/sprint/{sprint_id}/distraction")
async def log_distraction(sprint_id: str, distraction: str):
    """Log a distraction during sprint"""
    return {
        "sprint_id": sprint_id,
        "distraction": distraction,
        "timestamp": datetime.now()
    }


@router.post("/sprint/{sprint_id}/complete")
async def complete_sprint(sprint_id: str, retro: str):
    """Complete a sprint with retrospective"""
    return {
        "sprint_id": sprint_id,
        "completion_time": datetime.now(),
        "retrospective": retro,
        "status": "completed"
    }


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
